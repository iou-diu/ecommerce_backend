
import django_filters

from apps.user.forms import StaffUserFilterForm

from .models import StaffUser,CustomerUser

class StaffUserFilter(django_filters.FilterSet):
    class Meta:
        model = StaffUser
        fields = ['email']
        form = StaffUserFilterForm



class CustomerUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomerUser
        fields = ['email']
        form = StaffUserFilterForm
