import django_tables2 as tables
from apps.helpers import CustomTable
from apps.cms.models import Catalog, CorporateLead, NewsLetter

class CatalogTable(CustomTable):
    edit_url = 'catalog_update'
    delete_url = 'catalog_delete'
    detail_url = 'catalog_detail'  # This will be the "View Page" for products

    class Meta:
        model = Catalog
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['counter', 'title', 'tagline', 'slug', 'is_published', 'is_featured', 'published_date', 'action']
        empty_text = 'No catalogs available'
        orderable = True
        exclude = ('selected',)


class CorporateLeadTable(CustomTable):
    delete_url = 'corporate_lead_delete'
    detail_url = 'corporate_lead_detail'

    class Meta:
        model = CorporateLead
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['counter', 'company_name', 'contact_person', 'phone', 'email', 'project_type', 'status', 'created_at', 'action']
        empty_text = 'No corporate leads available'
        orderable = True
        exclude = ('selected',)


class NewsLetterTable(CustomTable):
    delete_url = 'newsletter_delete'

    class Meta:
        model = NewsLetter
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['counter', 'email', 'created_at', 'action']
        empty_text = 'No newsletter subscribers available'
        orderable = True
        exclude = ('selected',)
