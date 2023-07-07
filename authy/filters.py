from django.db.models import Q
import django_filters
from django.forms import TextInput
from .models import RenterInfo,PaymentLog

class SearchInput(TextInput):
    input_type = "search"

class RenterPaymentUniversalFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")
    class Meta:
        model = RenterInfo
        fields = ["query"]

    def universal_search(self,queryset,name,value):
        renterQuery =  RenterInfo.objects.filter(
            Q(renter__first_name__icontains=value) | Q(renter__last_name__icontains=value) |
            Q(payments__flat__flat_no__icontains=value)
        )
        return renterQuery