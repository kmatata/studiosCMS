from django.urls import path
from .views import owner,sales,renter,RenterInfoTableView,user_login,PaymentLogTableView


app_name = 'authy'

urlpatterns = [
    path('owner/',owner,name='ownerSignup'),
    path('sales/',sales,name='salesSignup'),
    path('renter/',renter,name='renterSignup'),
    path('login/',user_login,name='login'),
    path('sib-dash/',RenterInfoTableView.as_view(),name='tenant_table'),
    path('sib-payments/',PaymentLogTableView.as_view(), name='pmt_table'),
]