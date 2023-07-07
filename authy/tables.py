import django_tables2 as tables
from .models import RenterInfo, PaymentLog
from import_export import resources
from django.utils import timezone


class MyTenant(tables.Table):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = RenterInfo.objects.exclude(payments__isnull=True)
    class Meta:
        model = RenterInfo
        template_name = "django_tables2/bootstrap4.html" 

class PaymentLogTable(tables.Table):
    tenant = tables.Column(verbose_name='Tenant')
    created = tables.Column(verbose_name='created')
    updated = tables.Column(verbose_name='updated')
    payment_status = tables.Column(verbose_name='status')
    flat = tables.Column(accessor='flat.flat_no', verbose_name="Flat")
    water = tables.Column(accessor='water.get_cost', verbose_name="Water(KES)", order_by='water__quantity')
    sewage = tables.Column(accessor='sewage.get_cost', verbose_name="Sewage(KES)", order_by='sewage__quantity')
    rentalFee = tables.Column(accessor='flat.rentalFee', verbose_name='Rental Fee(KES)',order_by='flat__rentalFee')
    maintenance = tables.Column(accessor='flat.maintenaceFee',verbose_name='service fee(KES)',order_by='flat__maintenaceFee')
    total_cost = tables.Column(accessor='get_total_cost', verbose_name='Total Cost(KES)', orderable=False)
    class Meta:
        model = PaymentLog
        template_name = "tables/payments.html"
        attrs = {"class": "table table-striped"}
        exclude = ("id","renterInvoice")
        sequence = ("tenant","...")     
    
    def render_created(self, value):
        if value:
            return timezone.localtime(value).strftime('%Y-%m-%d %H:%M:%S')
        return ""

    def render_updated(self, value):
        if value:
            return timezone.localtime(value).strftime('%Y-%m-%d %H:%M:%S')
        return ""
    
    def render_water(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_sewage(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_rentalFee(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_maintenance(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_total_cost(self, value, record):
        return "{:,.0f}".format(value) if value else "" 

class RenterInfoTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = RenterInfo.objects.exclude(payments__isnull=True)

    renter = tables.Column(verbose_name="Renter")
    created2 = tables.Column(accessor='payments.last.updated', verbose_name="Date Paid", order_by='payments__updated')
    updated = tables.Column(accessor='payments.last.created', verbose_name="Invoice created", order_by='payments__created')
    payment_status = tables.Column(accessor='payments.last.payment_status', verbose_name="Payment Status", order_by='payments__payment_status')
    flat = tables.Column(accessor='payments.last.flat.flat_no', verbose_name="Flat", order_by='payments__flat__flat_no')
    water = tables.Column(accessor='payments.last.water.get_cost', verbose_name="Water(KES)", order_by='payments__water__quantity')
    sewage = tables.Column(accessor='payments.last.sewage.get_cost', verbose_name="Sewage(KES)", order_by='payments__sewage__quantity')
    rentalFee = tables.Column(accessor='payments.last.flat.rentalFee', verbose_name='Rental Fee(KES)',order_by='payments__flat__rentalFee')
    maintenance = tables.Column(accessor='payments.last.flat.maintenaceFee',verbose_name='service fee(KES)',order_by='payments__flat__maintenaceFee')
    total_cost = tables.Column(accessor='payments.last.get_total_cost', verbose_name='Total Cost(KES)', orderable=False)

    def render_created2(self, value):
        if value:
            return timezone.localtime(value).strftime('%Y-%m-%d %H:%M:%S')
        return ""

    def render_updated(self, value):
        if value:
            return timezone.localtime(value).strftime('%Y-%m-%d %H:%M:%S')
        return ""
    def render_renter(self, value, record):    
        return f"{record.renter.first_name} {record.renter.last_name}"     
    
    def render_water(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_sewage(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_rentalFee(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_maintenance(self, value, record):
        return "{:,.0f}".format(value) if value else ""

    def render_total_cost(self, value, record):
        return "{:,.0f}".format(value) if value else ""    

    class Meta:
        model = RenterInfo
        exclude = ("created","updated","id","renterImage_id")
        sequence = ("flat","...")
        template_name = "tables/tenant_table.html" 
        attrs = {"class": "table table-striped"}
    
