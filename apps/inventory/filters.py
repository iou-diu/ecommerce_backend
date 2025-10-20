import django_filters
from .models import PO, PurchaseOrder, Supplier
from .forms import PurchaseOrderFilterForm, SupplierFilterForm

class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = ['name',  'phone_number', 'email']
        form = SupplierFilterForm


class PurchaseOrderFilter(django_filters.FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = [
            'requisition', 'supplier', 'status', 
            'global_discount_type', 'purchase_tax_name', 'final_total_cost'
        ]
        form = PurchaseOrderFilterForm


class POFilter(django_filters.FilterSet):
    class Meta:
        model = PO
        fields = [
            'requisition', 'supplier', 'status', 
            'global_discount_type', 'purchase_tax_name', 'final_total_cost'
        ]
        form = PurchaseOrderFilterForm