from django.contrib import admin
from .models import Profile, RenterInfo, PaymentLog



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'is_staff', 'cell']
    list_filter = ['user', 'is_active',]
    raw_id_fields = ['user']
    search_fields = ['user']


@admin.register(RenterInfo)
class RenterAdmin(admin.ModelAdmin):
    list_display = ['renter', 'natId', 'taxinfo','renterImage_id']
    list_filter = ['renter','natId']
    search_fields = ['renter','natId']
    raw_id_fields = ['renter']
    date_hierarchy = 'created'
    ordering = ['updated']
    

@admin.register(PaymentLog)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'updated','payment_status','active','created']
    list_filter = ['tenant', 'payment_status']
    search_fields = ['tenant']    
    raw_id_fields = ['tenant']
    date_hierarchy = 'created'


    





