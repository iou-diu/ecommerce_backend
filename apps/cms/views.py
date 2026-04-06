from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_filters.views import FilterView

from apps.cms.models import HomeSlider, ContactForm, Catalog, CorporateLead, CorporateLeadActivity, NewsLetter
from apps.cms.forms import (
    HomeSliderForm, CatalogForm, CatalogFilterForm, 
    CorporateLeadForm, CorporateLeadFilterForm, CorporateLeadActivityForm
)
from apps.cms.tables import CatalogTable, CorporateLeadTable, NewsLetterTable
from apps.cms.filters import CatalogFilter, CorporateLeadFilter, NewsLetterFilter
from apps.helpers import PageHeaderMixin, CustomSingleTableMixin, MessageMixin, DeleteMessageMixin, PermissionRequiredMixin
from apps.ecom.models import Product
from django.db.models import Q


# Create your views here.
class HomeSliderView(ListView):
    model = HomeSlider
    template_name = 'cms/slider.html'

class HomeSliderCreateView(CreateView):
    model = HomeSlider
    form_class = HomeSliderForm
    template_name = 'cms/slider_form.html'
    success_url = reverse_lazy('home_slider')

class HomeSliderUpdateView(UpdateView):
    model = HomeSlider
    form_class = HomeSliderForm
    template_name = 'cms/slider_form.html'
    success_url = reverse_lazy('home_slider')

class HomeSliderDeleteView(DeleteView):
    model = HomeSlider
    template_name = 'cms/slider_confirm_delete.html'
    success_url = reverse_lazy('home_slider')


class ContactFormListView(ListView):
    model = ContactForm
    template_name = 'contacts-data.html'
    context_object_name = 'contacts'
    paginate_by = 20


def contact_form_ajax(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = ContactForm.objects.all()
    if search_value:
        queryset = queryset.filter(
            name__icontains=search_value
        )

    total = queryset.count()
    paginator = Paginator(queryset, length)
    page_number = start // length + 1
    page = paginator.get_page(page_number)

    data = []
    for contact in page.object_list:
        data.append([
            contact.name,
            contact.email,
            contact.phone,
            contact.subject,
            contact.message,
            contact.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': data
    })


class CatalogListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Catalog
    table_class = CatalogTable
    template_name = 'list.html'
    filterset_class = CatalogFilter
    page_title = 'All Catalogs'
    add_link = reverse_lazy('catalog_create')
    permission_required = 'cms.view_catalog'
    edit_url = 'catalog_update'
    delete_url = 'catalog_delete'
    detail_url = 'catalog_detail'


class CatalogCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Catalog
    form_class = CatalogForm
    template_name = 'add.html'
    success_url = reverse_lazy('catalog_list')
    page_title = 'Create Catalog'
    list_link = reverse_lazy('catalog_list')
    permission_required = 'cms.add_catalog'


class CatalogUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Catalog
    form_class = CatalogForm
    template_name = 'add.html'
    success_url = reverse_lazy('catalog_list')
    page_title = 'Update Catalog'
    list_link = reverse_lazy('catalog_list')
    permission_required = 'cms.change_catalog'


class CatalogDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Catalog
    template_name = 'delete.html'
    success_url = reverse_lazy('catalog_list')
    page_title = 'Delete Catalog'
    permission_required = 'cms.delete_catalog'


class CatalogDetailView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DetailView):
    model = Catalog
    template_name = 'cms/catalog_detail.html'
    page_title = 'Catalog Details & Product Management'
    permission_required = 'cms.view_catalog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catalog = self.object
        
        # Products currently in this catalog
        context['catalog_products'] = catalog.catalog_products.all()
        
        # Search for products to add
        search_query = self.request.GET.get('q', '')
        if search_query:
            context['search_products'] = Product.objects.filter(
                Q(name__icontains=search_query) | Q(slug__icontains=search_query)
            ).exclude(catalog=catalog)[:10]
        
        context['search_query'] = search_query
        return context

    def post(self, request, *args, **kwargs):
        catalog = self.get_object()
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        if product_id and action:
            product = get_object_or_404(Product, id=product_id)
            if action == 'add':
                product.catalog = catalog
                product.save()
                messages.success(request, f'Product "{product.name}" added to catalog.')
            elif action == 'remove':
                product.catalog = None
                product.save()
                messages.success(request, f'Product "{product.name}" removed from catalog.')
        
        return redirect('catalog_detail', pk=catalog.pk)

class CorporateLeadListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = CorporateLead
    table_class = CorporateLeadTable
    template_name = 'list.html'
    filterset_class = CorporateLeadFilter
    page_title = 'Corporate Inquiries (Leads)'
    permission_required = 'cms.view_corporatelead'
    delete_url = 'corporate_lead_delete'
    detail_url = 'corporate_lead_detail'


class CorporateLeadDetailView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = CorporateLead
    form_class = CorporateLeadForm
    template_name = 'cms/corporate_lead_detail.html'
    success_url = reverse_lazy('corporate_lead_list')
    page_title = 'Inquiry Details'
    list_link = reverse_lazy('corporate_lead_list')
    permission_required = 'cms.change_corporatelead'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity_form'] = CorporateLeadActivityForm()
        context['activities'] = self.object.activities.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Handle Activity Submission
        if 'submit_activity' in request.POST:
            activity_form = CorporateLeadActivityForm(request.POST)
            if activity_form.is_valid():
                activity = activity_form.save(commit=False)
                activity.lead = self.object
                activity.user = request.user
                activity.save()
                messages.success(request, "Activity recorded successfully.")
                return redirect('corporate_lead_detail', pk=self.object.pk)
        
        # Handle Lead Update (Status/Priority/Assigned)
        # We need to manually handle status change recording if changed
        old_status = self.object.status
        response = super().post(request, *args, **kwargs)
        
        # If lead was updated, check if status changed to log it automatically
        new_status = CorporateLead.objects.get(pk=self.object.pk).status
        if old_status != new_status:
            CorporateLeadActivity.objects.create(
                lead=self.object,
                user=request.user,
                activity_type='status_change',
                description=f"Status changed from {dict(self.object._meta.get_field('status').choices).get(old_status)} to {self.object.get_status_display()}"
            )
            
        return response


class CorporateLeadDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = CorporateLead
    template_name = 'delete.html'
    success_url = reverse_lazy('corporate_lead_list')
    page_title = 'Delete Lead'
    permission_required = 'cms.delete_corporatelead'


class NewsLetterListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = NewsLetter
    table_class = NewsLetterTable
    template_name = 'list.html'
    filterset_class = NewsLetterFilter
    page_title = 'Newsletter Subscribers'
    permission_required = 'cms.view_newsletter'
    delete_url = 'newsletter_delete'


class NewsLetterDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = NewsLetter
    template_name = 'delete.html'
    success_url = reverse_lazy('newsletter_list')
    page_title = 'Delete Subscriber'
    permission_required = 'cms.delete_newsletter'
