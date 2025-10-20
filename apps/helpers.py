from django.urls import reverse
import calendar
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.http import urlencode
import re
from django_tables2 import SingleTableMixin
import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe
import itertools
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
import typesense
from decouple import config
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
def choices_with_label(choices):
    return [("", "Select from items"), ] + list(choices)[1:]


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


def month_list():
    months = []
    for month_idx in range(1, 13):
        months.append((month_idx, calendar.month_name[month_idx]))
    return months


def day_list():
    day = []
    for index in range(1, 32):
        day.append((index, index))
    return day


def last_year_month():
    now = timezone.now()
    month = now.month - 1
    year = now.year
    if now.month == 1:
        month = 12
        year = now.year - 1
    return {
        'year': year,
        'month': month
    }


def u_slugify(txt):
    txt = txt.strip()  # remove trailing whitespace
    txt = re.sub('\s*-\s*', '-', txt, re.UNICODE)  # remove spaces before and after dashes
    txt = re.sub('[\s/]', '-', txt, re.UNICODE)  # replace remaining spaces with hyphens
    txt = re.sub('(\d):(\d)', r'\1-\2', txt, re.UNICODE)  # replace colons between numbers with dashes
    txt = re.sub('"', "", txt, re.UNICODE)  # replace double quotes with single quotes
    txt = re.sub('’', "", txt, re.UNICODE)
    txt = re.sub('‘', "", txt, re.UNICODE)
    txt = re.sub('\'', "", txt, re.UNICODE)
    txt = re.sub(r'[?,:!@#~`+=$%^&\\*()\[\]{}<>]', '', txt, re.UNICODE)  # remove some characters altogether
    return txt


class PermissionRequiredMixin(UserPassesTestMixin):
    permission_required = None

    def test_func(self):
        if self.permission_required is None:
            raise ValueError("You must set the 'permission_required' attribute on your view.")

        user = self.request.user
        if user.has_perm(self.permission_required):
            return True
        else:
            raise PermissionDenied


class PageHeaderMixin:
    page_title = None
    add_link = None
    list_link = None
    add_perms = None
    request = None
    show_selection = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        context['page_title'] = self.page_title
        context['show_selection'] = self.show_selection
        if self.add_link and self.request.user.has_perm(f'{content_type.app_label}.add_{content_type.model}'):
            context['add_link'] = self.add_link
        if self.list_link and self.request.user.has_perm(f'{content_type.app_label}.view_{content_type.model}'):
            context['list_link'] = self.list_link
        return context



class CustomSingleTableMixin(SingleTableMixin):
    request = None
    model = None
    detail_url = None
    edit_url = None
    delete_url = None

    def get_table_kwargs(self):
        ctx = super().get_table_kwargs()
        content_type = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        if self.detail_url:
            ctx['detail_url'] = self.detail_url
            ctx['view_perms'] = self.request.user.has_perm(f'{content_type.app_label}.view_{content_type.model}')
        if self.edit_url:
            ctx['edit_url'] = self.edit_url
            ctx['edit_perms'] = self.request.user.has_perm(f'{content_type.app_label}.change_{content_type.model}')
        if self.delete_url:
            ctx['delete_url'] = self.delete_url
            ctx['delete_perms'] = self.request.user.has_perm(f'{content_type.app_label}.delete_{content_type.model}')
        if not ctx.get('view_perms', False) and not ctx.get('edit_perms', False) and not ctx.get('delete_perms', False):
            return {'exclude': ('action',)}
        else:
            return ctx






class CustomTable(tables.Table):
    action = tables.Column(empty_values=(), orderable=False, attrs={
        'th': {'class': 'text-center'},
        'td': {
            'width': lambda value: len(value.split('</a> ')) * 55,
            'class': 'text-center'
        }
    })
    counter = tables.Column(empty_values=(), verbose_name='#', orderable=False)

    def __init__(self, *args, **kwargs):
        self.edit_perms = kwargs.pop('edit_perms', False)
        self.delete_perms = kwargs.pop('delete_perms', False)
        self.view_perms = kwargs.pop('view_perms', False)
        self.detail_url = kwargs.pop('detail_url', None)
        self.edit_url = kwargs.pop('edit_url', None)
        self.delete_url = kwargs.pop('delete_url', None)
        self.view_po = kwargs.pop('view_po', None)

        print(self.view_po)
        super().__init__(*args, **kwargs)

    def render_action(self, record):
        print(self.view_po)
        
        url = []
        if self.view_perms and self.detail_url:
            detail_url = reverse(self.detail_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-info"><i class="flaticon-eye"></i></a>' % detail_url)
        if self.edit_perms and self.edit_url:
            edit_url = reverse(self.edit_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-warning"><i class="flaticon-edit"></i></a>' % edit_url)
        if self.delete_perms and self.delete_url:
            del_url = reverse(self.delete_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-danger"><i class="flaticon-delete"></i></a>' % del_url)

        if  self.view_po:
            print("pooooooooo")
            view_po = reverse(self.view_po, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-danger"><i class="flaticon-eye"></i></a>' % view_po)

        return mark_safe(' '.join(url))

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
        return next(self.row_counter)




class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
        # return self.request.user.is_staff and self.request.user.groups.filter(name='boss').exists()

    def handle_no_permission(self):
        # Redirect to a custom page or login page
        return redirect(reverse_lazy('home'))
    

client = typesense.Client({
            'api_key': config('TYPESENSE_KEY'),
            'nodes': [{
                'host': config('TYPESENSE_IP'),
                'port': config('TYPESENSE_PORT'),
                'protocol': 'http'
            }],
            'connection_timeout_seconds': 2
        })


def u_slugify(txt):
    txt = txt.strip()  # remove trailing whitespace
    txt = re.sub('\s*-\s*', '-', txt, re.UNICODE)  # remove spaces before and after dashes
    txt = re.sub('[\s/]', '-', txt, re.UNICODE)  # replace remaining spaces with hyphens
    txt = re.sub('(\d):(\d)', r'\1-\2', txt, re.UNICODE)  # replace colons between numbers with dashes
    txt = re.sub('"', "", txt, re.UNICODE)  # replace double quotes with single quotes
    txt = re.sub('’', "", txt, re.UNICODE)
    txt = re.sub('‘', "", txt, re.UNICODE)
    txt = re.sub('\'', "", txt, re.UNICODE)
    txt = re.sub(r'[?,:!@#~`+=$%^&\\*()\[\]{}<>]', '', txt, re.UNICODE)  # remove some characters altogether
    return txt


# success or error message handler 



class MessageMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        model_name = self.model._meta.verbose_name  # Use verbose_name for a user-friendly model name
        
        # Determine the action and set the message
        if isinstance(self, CreateView):
            messages.success(self.request, f'{model_name.capitalize()} created successfully!')
        elif isinstance(self, UpdateView):
            messages.success(self.request, f'{model_name.capitalize()} updated successfully!')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        model_name = self.model._meta.verbose_name  # Use verbose_name for a user-friendly model name
        messages.error(self.request, f'There was an error {self.get_action()} {model_name}.')
        return response

    def get_action(self):
        """Helper method to get the action based on the view type."""
        if isinstance(self, CreateView):
            return "creating"
        elif isinstance(self, UpdateView):
            return "updating"
        return "processing"

class DeleteMessageMixin(MessageMixin):
    def get_success_url(self):
        model_name = self.model._meta.verbose_name  # Use verbose_name for a user-friendly model name
        messages.success(self.request, f'{model_name.capitalize()} deleted successfully!')
        return super().get_success_url()