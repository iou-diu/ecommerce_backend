from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML
from django.db.models import F, Sum
from apps.accounting.lookup import CustomSelect2Mixin
from apps.accounting.models import PaymentAccount
from apps.ecom.models import ProductVariant

from .models import (
    PurchasePayment, Supplier, Requisition, RequisitionItem,
    PurchaseOrder, PurchaseOrderItem,
    GoodsReceivedNote, GoodsReceivedItem
)


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['notes']

    def __init__(self, *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Form tag is in the template
        self.helper.layout = Layout(
            'notes',
        )


class ProductVariantSelect2Widget(CustomSelect2Mixin):
    model = ProductVariant
    queryset = ProductVariant.objects.all().order_by('id')
    search_fields = ['product__name__icontains', ]


class RequisitionItemForm(forms.ModelForm):
    class Meta:
        model = RequisitionItem
        fields = ['variant', 'quantity']
        widgets = {
            'variant': ProductVariantSelect2Widget(attrs={
                'data-minimum-input-length': 0,
            })
        }

    def __init__(self, *args, **kwargs):
        super(RequisitionItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Form tag is in the template
        self.helper.form_show_labels = False  # Labels are handled in the template
        self.fields['variant'].widget.attrs.update({'class': 'select2'})


RequisitionItemFormSet = inlineformset_factory(
    Requisition,
    RequisitionItem,
    form=RequisitionItemForm,
    fields=['variant', 'quantity'],
    extra=1,
    can_delete=False
)


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_delivery_date', 'notes']


PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    fields=['variant', 'quantity_ordered', 'price_per_unit'],
    extra=1,
    can_delete=True
)


class GoodsReceivedNoteForm(forms.ModelForm):
    class Meta:
        model = GoodsReceivedNote
        fields = ['notes']


GoodsReceivedItemFormSet = inlineformset_factory(
    GoodsReceivedNote,
    GoodsReceivedItem,
    fields=['variant', 'quantity_received'],
    extra=1,
    can_delete=True
)

# Test Formset
from django import forms
from django_select2.forms import ModelSelect2Widget
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from .models import TestStockLine, TestProduct


# Custom mixin to prevent multiple loading of Select2 JS/CSS
# Custom mixin to prevent multiple loading of Select2 JS/CSS
class CustomSelect2Widget(ModelSelect2Widget):
    @property
    def media(self):
        return forms.Media()


class TestStockLineForm(forms.ModelForm):
    class Meta:
        model = TestStockLine
        fields = ['product', 'quantity']
        widgets = {
            'product': CustomSelect2Widget(
                model=TestProduct.objects.all()[:10],  # Adjust to the number of default items
                search_fields=['name__icontains'],
                attrs={'data-placeholder': 'Select a product', 'style': 'width: 200px;'}
            )
        }


# Use modelformset_factory instead
TestStockLineFormSet = forms.modelformset_factory(
    model=TestStockLine,
    form=TestStockLineForm,
    extra=1,
    can_delete=True
)


# Main form (if needed)
class TestStockForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TestStockForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            'name', 'contact_type', 'contact_id', 'phone_number', 'alternate_contact_number',
            'landline', 'email', 'tax_number', 'opening_balance', 'pay_term_value',
            'pay_term_unit', 'address_line_1', 'address_line_2', 'city', 'state',
            'country', 'zip_code', 'image', 'trade_license', 'tin_certificate',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('contact_type', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('contact_id', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('alternate_contact_number', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('landline', css_class='form-group col-md-6 mb-0'),
                Column('tax_number', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('opening_balance', css_class='form-group col-md-6 mb-0'),
                Column('pay_term_value', css_class='form-group col-md-3 mb-0'),
                Column('pay_term_unit', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('address_line_1', css_class='form-group col-md-6 mb-0'),
                Column('address_line_2', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('country', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('trade_license', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('tin_certificate', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');"),
                    css_class='form-group col-md-12 text-center',
                ),
            ),
        )


# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ('name', 'contact_person', 'phone_number', 'email', 'address')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', 'contact_person', 'phone_number', 'email', 'address'),
#             ),
#             Row(
#                 Column(
#                    Submit('submit', 'Save', css_class='btn btn-primary', onclick="return confirm('Are you sure you want to submit?');")
#                 ),
#             )
#         )

class SupplierFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-2 mb-0'),

                Column('phone_number', css_class='form-group col-md-2 mb-0'),
                Column('email', css_class='form-group col-md-2 mb-0'),

                Column(Submit('filter', 'Filter'), css_class='form-group col-md-2 p-5 mt-2 mb-0'),
            ),
        )


class PurchaseOrderFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('requisition', css_class='form-group col-md-3 mb-0'),
                Column('supplier', css_class='form-group col-md-3 mb-0'),
                Column('status', css_class='form-group col-md-3 mb-0'),
                Column('global_discount_type', css_class='form-group col-md-3 mb-0'),
                Column('purchase_tax_name', css_class='form-group col-md-3 mb-0'),
                Column('final_total_cost', css_class='form-group col-md-3 mb-0'),
                Column(
                    HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                    css_class='form-group col-md-2 p-5 mb-0'
                ),
            ),
        )


class PurchasePaymentForm(forms.ModelForm):
    class Meta:
        model = PurchasePayment
        fields = (
            'purchase_order',
            'payment_account',
            'amount',
            'method',
            'status',
            'transaction_id',
            'document'
        )

    def __init__(self, *args, purchase_order=None, **kwargs):
        # purchase_order_instance = kwargs.pop('purchase_order_instance', None)
        super().__init__(*args, **kwargs)

        # 1. Restrict PurchaseOrder queryset to only those with a remaining balance
        self.fields['purchase_order'].queryset = (
            PurchaseOrder.objects
            .annotate(total_paid=Sum('purchaseorderpayments__amount'))
            .filter(
                final_total_cost__gt=F('total_paid') if 'total_paid' else 0
            )
        )

        self.fields['purchase_order'].disabled = True

        # 2. If a specific purchase_order_instance is passed, limit queryset and disable
        if purchase_order:  # Add a check to handle cases where purchase_order might be None
            self.fields['purchase_order'].queryset = PurchaseOrder.objects.filter(pk=purchase_order)
            self.fields['purchase_order'].disabled = True

        # 3. Only active payment accounts
        self.fields['payment_account'].queryset = PaymentAccount.objects.filter(is_active=True)

        # 4. Crispy form layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('purchase_order', css_class='form-group col-md-6 mb-0'),
                Column('payment_account', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('amount', css_class='form-group col-md-6 mb-0'),
                Column('method', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('transaction_id', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('document', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');"),
                    css_class='form-group col-md-12 text-right',
                )
            )
        )
