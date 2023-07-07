from celery import shared_task
from datetime import datetime, timedelta
from authy.models import RenterInfo,PaymentLog
from celery.utils.log import get_task_logger
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from SIB.celery import app
from celery.schedules import crontab
from django.http import HttpRequest
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
import weasyprint
import os

logger = get_task_logger(__name__)

# Create a mock request object
request = HttpRequest()

# Set the necessary attributes on the request object
request.method = 'GET'
request.META['SERVER_NAME'] = 'localhost'
request.META['SERVER_PORT'] = '8000'
request.META['HTTP_HOST'] = 'localhost:8000'
request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
request.user = User.objects.filter(groups__name='owner').first()

# Extract the necessary information from the request
email = request.user.email
url = request.build_absolute_uri('/flats/')

@app.task
def process_renter_info(url):
    # Get the queryset for active renter info objects        
    exp_date = datetime.now() - timedelta(days=30)
    tenants = RenterInfo.objects.filter(renter__is_active=True)  
    owner = User.objects.filter(groups__name='owner').first().email  
    for tenant in tenants:        
        last_payment = PaymentLog.objects.filter(tenant=tenant,updated__lt=exp_date,active=True).last()
        if last_payment:
            last_payment.active = False 
            last_payment.save()  
            # Send email to owner
            admin_subject = 'Update Invoicing Details'
            admin_message = f'Dear Admin,\n\nPlease update the invoicing details for the tenant: {tenant.renter.first_name} {tenant.renter.last_name}.'
            admin_message += f'\n\nYou can make the invoicing changes by visiting the following link:\n{url}'
            send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, [owner])
        
            logger.info("Task completed successfully")
        else:
            logger.info("No Task to work on yet")
            
# Schedule the task to run daily at a specific time
app.conf.beat_schedule = {
    'process_renter_info': {
        'task': 'flats.tasks.process_renter_info',
        'schedule': crontab(hour='23', minute='50'),  # Adjust the time as needed
        'args': (url,),  # Pass the URL as an argument
    },
}


@shared_task(name='send_invoice_email')
def send_invoice_email(payment_log_id):
    payment_log = PaymentLog.objects.get(id=payment_log_id)
    renter = payment_log.tenant.renter    
    subject = 'Invoice for Payment'
    message = 'Dear {},\n\nPlease find attached your invoice for the recent payment.'.format(renter.first_name)
    message += f'\n\n Your total payment for the month is {payment_log.get_total_cost}.'
    message += f'\n\n You can find more details by visiting the link:\n{url}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [renter.email]  # Assuming renter has an email field
    try:
        # Sending email
        email = EmailMessage(subject, message, email_from, recipient_list)
        out = BytesIO()
        html = render_to_string('pdfs/invoice2.html', {"paid": payment_log})
        css_path = os.path.join(settings.BASE_DIR, 'SIB/static/css/pdf.css')
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=[weasyprint.CSS(css_path)])
        email.attach(f'invoice_{payment_log.tenant.natId}.pdf',out.getvalue(),'application/pdf')
        email.send()
        logger.info('Invoice email sent successfully')  # Log success
    except Exception as e:
        logger.error('Failed to send invoice email: {}'.format(str(e)))  # Log error
    

