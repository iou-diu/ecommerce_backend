import django_filters
from apps.cms.models import Catalog, CorporateLead, NewsLetter
from apps.cms.forms import CatalogFilterForm, CorporateLeadFilterForm, NewsLetterFilterForm

class CatalogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Catalog
        fields = ['title', 'is_published', 'is_featured']
        form = CatalogFilterForm


class CorporateLeadFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(field_name='company_name', lookup_expr='icontains')
    class Meta:
        model = CorporateLead
        fields = ['company_name', 'status']
        form = CorporateLeadFilterForm
        
class NewsLetterFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    class Meta:
        model = NewsLetter
        fields = ['email']
        form = NewsLetterFilterForm
