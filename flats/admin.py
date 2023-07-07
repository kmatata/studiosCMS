from django.contrib import admin
from .models import Flat, Water, Sewage
from authy.models import PaymentLog

class PayemntInline(admin.TabularInline):
    model = PaymentLog
    list_display = ['tenant', 'created','payment_status','renterInvoice']
    
@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ['flat_no', 'vacant', 'rentalFee', 'maintenaceFee', 'threeMonthDeposit', 'nos_of_bedrooms']
    list_filter = ['flat_no', 'vacant','nos_of_bedrooms']    
    search_fields = ['flat_no']
    ordering = ['flat_no']  
    inlines = [PayemntInline]

@admin.register(Water)
class WaterAdmin(admin.ModelAdmin):
    list_display = ['unitPrice','quantity', 'flat']
    inlines = [PayemntInline]

@admin.register(Sewage)
class SewageAdmin(admin.ModelAdmin):
    list_display = ['unitPrice','quantity', 'flat']
    inlines = [PayemntInline]

