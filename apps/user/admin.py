from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.user.forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, AdminUser, Otp, StaffUser, CustomerUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ('-date_joined',)
    list_display = ('id','email', 'name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Groups', {'fields': ('groups',)}),  # Ensure this line is present
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

class AdminUserAdmin(CustomUserAdmin):
    model = AdminUser
    verbose_name = 'Admin'
    verbose_name_plural = 'Admins'
    list_display = ('email', 'name', 'is_staff', 'is_superuser')

class StaffUserAdmin(CustomUserAdmin):
    model = StaffUser
    verbose_name = 'Staff'
    verbose_name_plural = 'Staff Members'
    list_display = ('email', 'name', 'is_staff')


class CustomerUserAdmin(CustomUserAdmin):
    model = CustomerUser
    verbose_name = 'Student'
    verbose_name_plural = 'Students'
    list_display = ('email', 'name')

# Register the admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(StaffUser, StaffUserAdmin)
admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(Otp)

