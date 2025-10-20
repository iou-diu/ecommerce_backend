
import django_filters

from .models import Address, Attribute, AttributeValue, Brand, Category, FlashDeal, Product, ProductImage, ProductVariant, StockEntry, Tag, Tax

from .forms import AddressFilterForm, AttributeFilterForm, AttributeValueFilterForm, BrandFilterForm, CategoryFilterForm, FlashDealFilterForm, ProductFilterForm, ProductImageFilterForm, ProductVariantFilterForm, StockEntryFilterForm, TagFilterForm, TaxFilterForm

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Category
        fields = ['name', 'parent','is_featured','is_active', 'for_product', 'for_solution']
        form = CategoryFilterForm



class AddressFilter(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = ['user', 'full_name', 'address_line_1', 'address_line_2', 'city', 'state_or_province', 'postal_code', 'country', 'phone_number', 'is_default_shipping', 'is_default_billing']
        form = AddressFilterForm



class BrandFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Brand
        fields = ['name', 'description', 'meta_title', 'meta_description', 'slug', 'is_active']
        form = BrandFilterForm



class AttributeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Attribute
        fields = ['name', 'data_type', 'unit', 'is_filterable', 'is_variation']
        form = AttributeFilterForm



class AttributeValueFilter(django_filters.FilterSet):
    value = django_filters.CharFilter(field_name='value', lookup_expr='icontains')
    
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'value']
        form = AttributeValueFilterForm



class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Tag
        fields = ['name']
        form = TagFilterForm



class TaxFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Tax
        fields = ['name', 'tax_type', 'is_active']
        form = TaxFilterForm



class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand']
        form = ProductFilterForm


class ProductImageFilter(django_filters.FilterSet):
    class Meta:
        model = ProductImage
        fields = ['product',]
        form = ProductImageFilterForm


class ProductVariantFilter(django_filters.FilterSet):
    class Meta:
        model = ProductVariant
        fields = ['product', 'sku', 'upc']
        form = ProductVariantFilterForm



class StockEntryFilter(django_filters.FilterSet):
    class Meta:
        model = StockEntry
        fields = ['variant']
        form = StockEntryFilterForm

from .models import Order

from .forms import OrderFilterForm

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['user', 'shipping_address', 'billing_address', 'shipping_method', 'coupon', 'status', 'subtotal', 'shipping_cost', 'total_discount', 'total_amount', 'payment_status', 'created_at', 'updated_at', 'notes']
        form = OrderFilterForm


class FlashDealFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Search by Title')

    class Meta:
        model = FlashDeal
        fields = ['title']
        form = FlashDealFilterForm
