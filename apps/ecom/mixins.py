# forms.py

from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

from apps.lookup import CustomSelect2Mixin, CustomSelect2MultipleMixin
from .models import  Attribute, AttributeValue, Category,Brand,Tag


class AttributeWidget(CustomSelect2Mixin):
    model = Attribute
    search_fields = ['name__icontains']

class AttributeValueWidget(CustomSelect2MultipleMixin):
    model = AttributeValue
    search_fields = ['value__icontains']
    dependent_fields = {'attribute': 'attribute'}

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        queryset = super().filter_queryset(request, term, queryset, **dependent_fields)
        attribute_id = dependent_fields.get('attribute')
        if attribute_id:
            queryset = queryset.filter(attribute_id=attribute_id)
        return queryset


class CategoryWidget(CustomSelect2Mixin):
    model = Category
    search_fields = ['name__icontains']


class BrandWidget(CustomSelect2Mixin):
    model = Brand
    search_fields = ['name__icontains']

class TagMultipleSelect2Widget(CustomSelect2MultipleMixin):
    model = Tag
    queryset = Tag.objects.all().order_by('name')
    search_fields = ['name__icontains', ]