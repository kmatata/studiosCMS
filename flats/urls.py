from django.urls import path
from .views import (
    allFlats,updatePropertyCosts,rent_a_flat_at_sib
    ,change_flat_status_and_remove_tenant,
    create_send_invoice_to_tenant,tenant_renew_lease,
    update_tenant_details
    )
app_name = 'flats'

urlpatterns = [    
    path('update-tenant/',update_tenant_details),
    path('',allFlats,name='allFlats'),
    path('update-property-cost/',updatePropertyCosts,
         name='cost-update'),
    path('new-tenant/',rent_a_flat_at_sib,name='new-tenant'),
    path('deactivate-tenant/',
         change_flat_status_and_remove_tenant,
         name='deactivate'),
    path('invoicing/',create_send_invoice_to_tenant,
         name='invoicing'),
    path('renew-lease/',tenant_renew_lease,name='renew-lease')
]