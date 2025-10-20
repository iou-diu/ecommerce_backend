# Standard Library Imports
from django.utils import timezone
from django.utils.timesince import timesince

# Django Imports
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.db.models import Count, Sum
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

# Custom Imports
from apps.helpers import CustomSingleTableMixin, PageHeaderMixin, PermissionRequiredMixin

# Application Imports
from apps.accounting.models import Bill
from apps.user.forms import GroupPermissionForm
from .models import CustomerUser, StaffUser
from .forms import CustomerUserForm, GroupPermissionForm, StaffUserForm
from .tables import CustomerUserTable, StaffUserTable
from .filters import CustomerUserFilter, StaffUserFilter


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        User = get_user_model()
        staff_admin_users = User.objects.filter(is_staff=True, last_login__isnull=False).order_by('-last_login')
        recent_logins = []
        for user in staff_admin_users:
            login_time_ago = timesince(user.last_login, timezone.now()) + ' ago'
            recent_logins.append({
                'email': user.email,
                'last_login_time': login_time_ago,
            })

        context['recent_logins'] = recent_logins

        # Total Due Amount
        total_due = Bill.objects.aggregate(total_due=Sum('total_due'))['total_due'] or 0
        context['total_due'] = total_due

        # Total Collection (Total Paid)
        total_paid = Bill.objects.aggregate(total_paid=Sum('total_paid'))['total_paid'] or 0
        context['total_paid'] = total_paid

        return context


@user_passes_test(lambda u: u.is_superuser)
def group_permission_view(request):
    # Check if the form is being submitted via GET or POST
    if request.method == 'POST':
        form = GroupPermissionForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            selected_permissions = request.POST.getlist('permissions')
            group.permissions.clear()
            group.permissions.set(selected_permissions)
            messages.success(request, "Permissions updated successfully.")
            return redirect('group_permission_view')
    else:
        form = GroupPermissionForm(request.GET)  # Use GET data to bind the form
        group = None
        if form.is_valid():
            group = form.cleaned_data['group']

    permissions = Permission.objects.all().select_related('content_type')
    grouped_permissions = {}

    for perm in permissions:
        app_label = perm.content_type.app_label
        model_name = perm.content_type.model
        action = perm.codename.split('_')[0]

        if app_label not in grouped_permissions:
            grouped_permissions[app_label] = {}

        if model_name not in grouped_permissions[app_label]:
            grouped_permissions[app_label][model_name] = {
                'create': None, 'view': None, 'change': None, 'delete': None
            }

        if action == 'add':
            grouped_permissions[app_label][model_name]['create'] = perm
        elif action == 'view':
            grouped_permissions[app_label][model_name]['view'] = perm
        elif action == 'change':
            grouped_permissions[app_label][model_name]['change'] = perm
        elif action == 'delete':
            grouped_permissions[app_label][model_name]['delete'] = perm

    # Only retrieve permissions if a group is selected
    group_permissions = group.permissions.all() if group else []

    return render(request, 'group_permissions_table.html', {
        'form': form,
        'grouped_permissions': grouped_permissions,
        'group_permissions': group_permissions,
    })


class StaffUserListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                        FilterView):
    model = StaffUser
    table_class = StaffUserTable
    template_name = 'list.html'
    permission_required = 'user.view_staffuser'
    filterset_class = StaffUserFilter
    page_title = 'All Staff'
    add_link = reverse_lazy('staffuser_add')
    add_perms = 'user.add_staffuser'
    edit_perms = 'user.change_staffuser'
    delete_perms = 'user.delete_staffuser'
    edit_url = 'staffuser_update'
    delete_url = 'staffuser_delete'


class StaffUserCreateView(PermissionRequiredMixin, PageHeaderMixin, LoginRequiredMixin, CreateView):
    model = StaffUser
    form_class = StaffUserForm
    template_name = 'add.html'
    permission_required = 'user.add_staffuser'
    success_url = reverse_lazy('staffuser_list')
    page_title = 'Staff'
    list_link = reverse_lazy('staffuser_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Staff user created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the staff user.")
        return super().form_invalid(form)


class StaffUserUpdateView(PermissionRequiredMixin, PageHeaderMixin, LoginRequiredMixin, UpdateView):
    model = StaffUser
    form_class = StaffUserForm
    template_name = 'add.html'
    permission_required = 'user.change_staffuser'
    success_url = reverse_lazy('staffuser_list')
    page_title = 'Update Staff'
    list_link = reverse_lazy('staffuser_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Staff user updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the staff user.")
        return super().form_invalid(form)


class StaffUserDeleteView(PermissionRequiredMixin, PageHeaderMixin, LoginRequiredMixin, DeleteView):
    model = StaffUser
    template_name = 'delete.html'
    permission_required = 'user.delete_staffuser'
    page_title = 'Delete Staff'

    # success_url = reverse_lazy('staffuser_list')

    def get_success_url(self):
        messages.success(self.request, "Staff user deleted successfully.")
        return reverse_lazy('staffuser_list')


class CustomerUserListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                           FilterView):
    model = CustomerUser
    table_class = CustomerUserTable
    template_name = 'list.html'
    permission_required = 'user.view_customeruser'
    filterset_class = CustomerUserFilter
    page_title = 'All Customer'
    add_link = reverse_lazy('customeruser_add')
    add_perms = 'user.add_customeruser'
    edit_perms = 'user.change_customeruser'
    delete_perms = 'user.delete_customeruser'
    # edit_url = 'customeruser_update'
    # delete_url = 'customeruser_delete'


class CustomerUserCreateView(PermissionRequiredMixin, PageHeaderMixin, LoginRequiredMixin, CreateView):
    model = CustomerUser
    form_class = CustomerUserForm
    template_name = 'add.html'
    permission_required = 'user.add_customeruser'
    success_url = reverse_lazy('customeruser_list')
    page_title = 'Customer'
    list_link = reverse_lazy('customeruser_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Customer user created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the Customer user.")
        return super().form_invalid(form)


class CustomerUserUpdateView(PermissionRequiredMixin, PageHeaderMixin, LoginRequiredMixin, UpdateView):
    model = CustomerUser
    form_class = CustomerUserForm
    template_name = 'add.html'
    permission_required = 'user.change_customeruser'
    success_url = reverse_lazy('customeruser_list')
    page_title = 'Update Customer'
    list_link = reverse_lazy('customeruser_list')


class CustomerUserDeleteView(PermissionRequiredMixin, PageHeaderMixin, LoginRequiredMixin, DeleteView):
    model = CustomerUser
    template_name = 'delete.html'
    permission_required = 'user.delete_customeruser'
    page_title = 'Delete Customer'
    success_url = reverse_lazy('customeruser_list')


from django.http import HttpResponseRedirect
from django.views import View
from urllib.parse import urlencode

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class PaymentHandlerView(View):
    def dispatch(self, request, *args, **kwargs):
        """
        Handle both GET and POST requests.
        """
        # Extract order information
        order_id = request.GET.get('order_verify') or request.POST.get('order_verify')

        if not order_id:
            frontend_url = f"https://daffodilrobotics.com?{urlencode({'order_verify': order_id})}"
            return HttpResponseRedirect(frontend_url)

        # Redirect to the frontend with the order_id
        frontend_url = f"https://daffodilrobotics.com/order_verify?{urlencode({'order_verify': order_id})}"
        return HttpResponseRedirect(frontend_url)
