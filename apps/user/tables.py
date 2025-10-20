from apps.helpers import CustomTable

from .models import StaffUser,CustomerUser

class StaffUserTable(CustomTable):
    edit_url = 'staffuser_update'
    delete_url = 'staffuser_delete'
    class Meta:
        model = StaffUser
        template_name = 'django_tables2/bootstrap4.html'
        fields = [ 'last_login', 'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email', 'name', 'customuser_ptr']



class CustomerUserTable(CustomTable):
    edit_url = 'customeruser_update'
    delete_url = 'customeruser_delete'
    class Meta:
        model = CustomerUser
        template_name = 'django_tables2/bootstrap4.html'
        fields = [ 'name', 'email','last_login',  ]
