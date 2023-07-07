from django.shortcuts import render
from .models import Flat,Water,Sewage
from authy.models import RenterInfo,PaymentLog,Profile
from django.db.models import Q
import json
from collections import defaultdict
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.models import User
from .tasks import send_invoice_email
import re

def allFlats(request):
    myFlat = None
    myPendingFlat = None
    new_user = None
    current_user = User.objects.get(id=request.user.id)
    occupied_flats = PaymentLog.objects.filter(active=True,payment_status='complete')
    vacant_flats = Flat.objects.filter(vacant=True)
    pending_flats = PaymentLog.objects.filter(active=False,
                                              tenant__renter__is_active=True,payment_status='complete',
                                              flat__isnull=False
                                              )
    flats = Flat.objects.all()
    try:
        if current_user.renterProfile:
            myFlat = PaymentLog.objects.get(tenant__renter=current_user,active=True,payment_status='complete')

    except:
        pass
    try:        
        if current_user.renterProfile:
            myPendingFlat = PaymentLog.objects.get(tenant__renter=current_user,active=True,payment_status='pending')
    except:
        pass
    try:
        if not current_user.renterProfile.payments.values().exists():
            new_user = RenterInfo.objects.get(renter=current_user)
    except:
        pass
    tenants = RenterInfo.objects.filter(Q(payments__isnull=False) & 
                                        Q(renter__is_active=True) & 
                                        Q(payments__flat__isnull=False)
                                        )
    new_tenants = RenterInfo.objects.filter(Q(payments__isnull=True) & 
                                        Q(renter__is_active=True) & 
                                        Q(payments__flat__isnull=True)
                                        )
    context = {"occupied_flats":occupied_flats,
               "myFlat":myFlat,
               "new_user":new_user,
               "myPendingFlat":myPendingFlat,
               "vacant_flats":vacant_flats,
               "pending_flats":pending_flats,
               "flats":flats,
               "tenants":tenants,
               "renters":new_tenants,
               "current_user":current_user}
    return render(request,'main-html/sib_main.html',context)

#admin views


def is_valid_decimal(value):
    # Regular expression pattern for a valid decimal number
    pattern = r'^-?\d+(\.\d+)?$'
    return re.match(pattern, value) is not None


def updatePropertyCosts(request):
    data = json.loads(request.body)
    
    flat = Flat.objects.get(flat_no=data['flat_no'])
    if flat:
        if data['rentalFee']:
            flat.rentalFee = Decimal(re.sub(r"[^\d.]", "",data['rentalFee']))
        if data['deposit']:
            flat.threeMonthDeposit = Decimal(re.sub(r"[^\d.]", "",data['deposit']))
        if data['serviceFee']:
            flat.maintenaceFee = Decimal(re.sub(r"[^\d.]", "",data['serviceFee']))
        if data['water_unit_cost'] and is_valid_decimal(data['water_unit_cost']):
            flat.waterUnitCost = Decimal(data['water_unit_cost'])
        if data['sewage_unit_cost'] and is_valid_decimal(data['sewage_unit_cost']):
            flat.sewageUnitCost = Decimal(data['sewage_unit_cost'])
        flat.save()
        return JsonResponse('Flat info updated successfully',safe=False)
    return JsonResponse('Error updating flat info',safe=False)

#tenant views
def rent_a_flat_at_sib(request):
    payment_deets = defaultdict(list)
    natId_file_data = request.FILES.get('renter_natId_image')
    taxInfo_file_data = request.FILES.get('renter_taxInfo_image')
    flat_to_rent = Flat.objects.get(flat_no=request.POST.get('flat_no'),vacant=True,depositPaid=False)
    renter = RenterInfo.objects.get(renter__email=request.POST.get('email'))
    profile_renter = Profile.objects.get(user__email=request.POST.get('email'))
    if renter:
        renter.natId = request.POST.get('nat_id')
        renter.taxinfo = taxInfo_file_data
        renter.renterImage_id = natId_file_data
        profile_renter.cell = request.POST.get('cell_nos')
        profile_renter.save()
        renter.save()
        payment = PaymentLog.objects.create(tenant=renter,flat=flat_to_rent,active=True)        
        payment_deets['deposit'].append(flat_to_rent.threeMonthDeposit)
        payment_deets['rent'].append(flat_to_rent.rentalFee)
        payment_deets['flat'].append(flat_to_rent.flat_no)
        payment_deets['bedrooms'].append(flat_to_rent.nos_of_bedrooms)
        payment_deets['ttl_payable'].append(payment.get_total_cost)
        payment_deets['first_last_name'].append(f"{renter.renter.first_name} {renter.renter.last_name}")
        payment_deets['email'].append(renter.renter.email)
        payment_deets['cell'].append(f"+{renter.renter.profile.cell.country_code} {renter.renter.profile.cell.national_number}")
        payment_deets['payLog'].append(payment.id)
        return JsonResponse(payment_deets,safe=False)
    return JsonResponse('error occured please try again later!',safe=False)

#admin views
def update_tenant_details(request):
    if request.method == 'POST':
        renter_natId_image = request.FILES.get('renter_natId_image')
        renter_taxInfo_image = request.FILES.get('renter_taxInfo_image')
        nat_id = request.POST.get('nat_id')
        print(nat_id)
        cell_nos = request.POST.get('cell_nos')
        renter = RenterInfo.objects.get(natId=nat_id)
        if renter:
            renter.natId = nat_id
            if renter_taxInfo_image:
                renter.taxinfo = renter_taxInfo_image
            if renter_natId_image:
                renter.renterImage_id = renter_natId_image
            renter.renter.profile.cell = cell_nos
            renter.save()
            return JsonResponse('Tenant info updated successfully',safe=False)
    return JsonResponse('Error updating Tenant info',safe=False)

#tenant views
def tentant_makes_first_rent_payment(request):
    data = json.loads(request.body)    
    payable = PaymentLog.objects.get(id=data['payLog'])
    payable.payment_status = 'complete'
    payable.save()
    flat = Flat.objects.get(flat_no=data['flat_no'])
    flat.vacant = False
    flat.depositPaid = True
    flat.save()
    return JsonResponse('success',safe=False)
#admin views
def change_flat_status_and_remove_tenant(request):
    data = json.loads(request.body)
    tenant = RenterInfo.objects.get(natId=data['nat_id'])
    tenant.renter.is_active = False
    tenant.save()
    flat = Flat.objects.get(flat_no=data['flat_no'])
    flat.vacant = True
    flat.depositPaid = False
    flat.save()
    return JsonResponse("success",safe=False)
#admin views
def create_send_invoice_to_tenant(request):
    data = json.loads(request.body)
    invoice_data = defaultdict(list)
    flat = Flat.objects.get(flat_no=data['flat_no'])
    flat.waterUnitCost = Decimal(data['water_unit_cost'])
    flat.sewageUnitCost = Decimal(data['sewage_unit_cost'])
    flat.maintenaceFee = Decimal(re.sub(r"[^\d.]", "",data['serviceFee']))
    flat.rentalFee = Decimal(re.sub(r"[^\d.]", "",data['rentalFee']))
    flat.save()
    water = Water.objects.create(flat=flat,unitPrice=flat.waterUnitCost,quantity=data['water_qtty'])
    sewage = Sewage.objects.create(flat=flat,unitPrice=flat.sewageUnitCost,quantity=data['sewage_qtty'])
    renter = RenterInfo.objects.get(natId=data['nat_id'])
    payment = PaymentLog.objects.create(tenant=renter,active=True,flat=flat,water=water,sewage=sewage)    
    invoice_data['flat'].append(flat.flat_no)
    invoice_data['water_unit_cost'].append(water.unitPrice)
    invoice_data['water_qtty_used'].append(water.quantity)
    invoice_data['water_payable'].append(water.get_cost)
    invoice_data['sewage_unit_cost'].append(sewage.unitPrice)
    invoice_data['sewage_qtty_used'].append(sewage.quantity)
    invoice_data['sewage_payable'].append(sewage.get_cost)
    invoice_data['flat_rent'].append(flat.rentalFee)
    invoice_data['total_payable'].append(payment.get_total_cost)
    invoice_data['paylog_id'].append(payment.id)
    send_invoice_email.delay(payment.id)
    return JsonResponse(f"invoice sent to {payment.tenant.renter.email}",safe=False)
#tenant views
def tenant_renew_lease(request):
    data = json.loads(request.body)
    payable = PaymentLog.objects.get(id=data['paylog_id'])
    payable.payment_status = 'complete'
    payable.save()
    return JsonResponse('successfully renewed',safe=False)




        



    





        


