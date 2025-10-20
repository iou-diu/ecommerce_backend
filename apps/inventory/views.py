from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# views.py
from django_filters.views import FilterView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.ecom.models import ProductVariant
from apps.helpers import CustomSingleTableMixin, DeleteMessageMixin, MessageMixin, PageHeaderMixin
from apps.inventory.filters import POFilter, PurchaseOrderFilter, SupplierFilter
from apps.inventory.models import PO, PurchaseOrder, PurchasePayment, Requisition, RequisitionItem, Supplier, \
    TestStockLine
from apps.inventory.tables import POTable, PurchaseOrderTable, RequisitionTable, SupplierTable
from .forms import GoodsReceivedNoteForm, PurchaseOrderForm, PurchasePaymentForm, RequisitionForm, \
    RequisitionItemFormSet, PurchaseOrderItemFormSet, GoodsReceivedItemFormSet, SupplierForm, TestStockForm, \
    TestStockLineForm
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
import json
from django.core.serializers import serialize
from django.contrib import messages


class RequisitionListView(PageHeaderMixin, CustomSingleTableMixin, ListView):
    model = Requisition
    table_class = RequisitionTable
    template_name = 'list.html'

    # ordering = ['some_field']
    page_title = 'All Requisition'
    add_link = reverse_lazy('create_requisition')
    add_perms = 'requisition.add_requisition'


@login_required
def approve_requisition(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    if not requisition.approved:  # Only approve if not already approved
        requisition.approved = True
        requisition.approved_by = request.user  # Assuming the logged-in user approves it
        requisition.save()
    return redirect(reverse('requisition_list'))  # Redirect back to the requisition list


@login_required
# def requisition_detail(request, pk):
#     requisition = get_object_or_404(Requisition, pk=pk)
#     page_title = f'Requisition {requisition.id} Details'

#     return render(request, 'requisition_detail.html', {
#         'requisition': requisition,
#         'page_title': page_title
#     })
def requisition_detail(request, requisition_id):
    requisition = get_object_or_404(Requisition, id=requisition_id)

    # Modify the field from 'variant__name' to a valid field in ProductVariant, e.g., 'variant__sku'
    items = list(requisition.items.all().values('id', 'variant__sku', 'quantity'))

    context = {
        'requisition': requisition,
        'items': items
    }
    print(context)
    return render(request, 'requisition_detail.html', context)


@login_required
def create_requisition(request):
    page_title = 'Requisition'
    list_link = reverse_lazy('requisition_list')
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        formset = RequisitionItemFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            requisition = form.save(commit=False)
            requisition.requested_by = request.user
            requisition.save()
            formset.instance = requisition
            formset.save()
            messages.success(request, 'Requisition created successfully!')
            return redirect('requisition_list')
        else:
            messages.error(request, 'There was an error creating the requisition. Please correct the errors below.')
    else:
        form = RequisitionForm()
        formset = RequisitionItemFormSet(prefix='items', queryset=RequisitionItem.objects.none())

    return render(request, 'requisition_form.html', {
        'form': form,
        'formset': formset,
        'page_title': page_title,
        'list_link': list_link
    })


@login_required
def edit_requisition(request, requisition_id):
    requisition = get_object_or_404(Requisition, id=requisition_id)
    page_title = 'Edit Requisition'
    list_link = reverse_lazy('requisition_list')

    if request.method == 'POST':
        form = RequisitionForm(request.POST, instance=requisition)
        formset = RequisitionItemFormSet(request.POST, instance=requisition, prefix='items')

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Requisition updated successfully!')
            return redirect('requisition_list')
        else:
            messages.error(request, 'There was an error updating the requisition. Please correct the errors below.')
    else:
        form = RequisitionForm(instance=requisition)
        formset = RequisitionItemFormSet(instance=requisition, prefix='items')

    return render(request, 'requisition_form.html', {
        'form': form,
        'formset': formset,
        'page_title': page_title,
        'list_link': list_link,
        'requisition': requisition,
    })


@login_required
def create_purchase_order(request, requisition_id):
    requisition = get_object_or_404(Requisition, id=requisition_id)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.requisition = requisition
            purchase_order.save()
            formset.instance = purchase_order
            formset.save()
            return redirect('purchase_order_detail', pk=purchase_order.pk)
    else:
        form = PurchaseOrderForm()
        # Initialize formset with requisition items
        initial_data = [
            {'variant': item.variant, 'quantity_ordered': item.quantity}
            for item in requisition.items.all()
        ]
        formset = PurchaseOrderItemFormSet(initial=initial_data)
    return render(request, 'purchase_order_form.html', {'form': form, 'formset': formset, 'requisition': requisition})


@login_required
def create_goods_received_note(request, purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id, status='ordered')
    if request.method == 'POST':
        form = GoodsReceivedNoteForm(request.POST)
        formset = GoodsReceivedItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            grn = form.save(commit=False)
            grn.purchase_order = purchase_order
            grn.save()
            formset.instance = grn
            formset.save()
            # Update stock levels and create stock entries here
            # Optionally, update the purchase order status to 'received'
            return redirect('goods_received_note_detail', pk=grn.pk)
    else:
        form = GoodsReceivedNoteForm()
        initial_data = [
            {'variant': item.variant, 'quantity_received': item.quantity_ordered}
            for item in purchase_order.items.all()
        ]
        formset = GoodsReceivedItemFormSet(initial=initial_data)
    return render(request, 'goods_received_note_form.html',
                  {'form': form, 'formset': formset, 'purchase_order': purchase_order})


from .forms import TestStockLineFormSet


def add__test_stock(request):
    if request.method == 'POST':
        form = TestStockForm(request.POST)
        formset = TestStockLineFormSet(request.POST, queryset=TestStockLine.objects.none())
        if formset.is_valid():
            formset.save()
            return redirect('add__test_stock')  # Replace with your success URL
    else:
        form = TestStockForm()
        formset = TestStockLineFormSet(queryset=TestStockLine.objects.none())

    return render(request, 'add_stock.html', {'form': form, 'formset': formset})


@login_required(login_url='login')
def purchase_order_form(request):
    return render(request, 'po_before_purchase.html')


@login_required(login_url='login')
def po_form(request):
    return render(request, 'po_form.html')


@login_required(login_url='login')
def po_form_edit(request, pk):
    # Retrieve the purchase order or return 404 if not found
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if purchase_order.status == 'delivered':
        messages.error(request, 'Edit is not allowed for Delivered Purchase Order. You can view it only.')
        # Redirect to the purchase order display view
        return redirect('purchase_order_display', pk=pk)

    # Pass the purchase_order_id to the template
    context = {
        'purchase_order_id': purchase_order.id,
    }

    return render(request, 'po_form_edit.html', context)


@login_required(login_url='login')
def po_display(request, pk):
    # Retrieve the purchase order or return 404 if not found
    purchase_order = get_object_or_404(PO, pk=pk)

    # Pass the purchase_order_id to the template
    context = {
        'purchase_order_id': purchase_order.id,
    }

    return render(request, 'po_display.html', context)


@login_required(login_url='login')
def purchase_display(request, pk):
    # Retrieve the purchase order or return 404 if not found
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)

    # Pass the purchase_order_id to the template
    context = {
        'purchase_order_id': purchase_order.id,
    }

    return render(request, 'purchase_display.html', context)


@login_required(login_url='login')
def po_new(request):
    return render(request, 'po_new.html')


# Supplier crud model

class SupplierListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                       FilterView):
    model = Supplier
    table_class = SupplierTable
    template_name = 'list.html'
    permission_required = 'yourapp.view_supplier'
    filterset_class = SupplierFilter
    page_title = 'All Suppliers'
    add_link = reverse_lazy('supplier_add')
    add_perms = 'yourapp.add_supplier'
    edit_perms = 'yourapp.change_supplier'
    delete_perms = 'yourapp.delete_supplier'
    edit_url = 'supplier_update'
    delete_url = 'supplier_delete'


class SupplierCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'add.html'
    permission_required = 'yourapp.add_supplier'
    success_url = reverse_lazy('supplier_list')
    page_title = 'Add Supplier'
    list_link = reverse_lazy('supplier_list')


class SupplierUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'add.html'
    permission_required = 'yourapp.change_supplier'
    success_url = reverse_lazy('supplier_list')
    page_title = 'Update Supplier'
    list_link = reverse_lazy('supplier_list')


class SupplierDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Supplier
    template_name = 'delete.html'
    permission_required = 'yourapp.delete_supplier'
    page_title = 'Delete Supplier'
    success_url = reverse_lazy('supplier_list')


# POS module
@login_required(login_url='login')
def pos_form(request):
    return render(request, 'pos_form.html')


class POListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = PO
    table_class = POTable
    template_name = 'list.html'
    permission_required = 'ecom.view_po'
    filterset_class = POFilter
    page_title = 'All Purchase Orders'
    add_link = reverse_lazy('purchase_order_create')
    add_perms = 'purchaseorder.add_supplier'
    # edit_perms = 'purchaseorder.change_purchaseorder'
    edit_url = 'po_details_display'
    view_po = 'po_details_display'

    # def get_table_kwargs(self):
    #     kwargs = super().get_table_kwargs()
    #     kwargs.update({
    #         # 'edit_perms': self.request.user.has_perm('purchaseorder.change_purchaseorder'),
    #         # 'delete_perms': self.request.user.has_perm('purchaseorder.delete_purchaseorder'),
    #         'view_perms': self.request.user.has_perm('purchaseorder.view_purchaseorder'),
    #         'detail_url': self.detail_url,
    #         'edit_url': self.edit_url,
    #         'delete_url': self.delete_url,
    #         'view_po': self.view_po,  # Pass view_po here
    #     })
    #     return kwargs


class PurchaseOrderListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                            FilterView):
    model = PurchaseOrder
    table_class = PurchaseOrderTable
    template_name = 'list.html'
    permission_required = 'ecom.view_purchaseorder'
    filterset_class = PurchaseOrderFilter
    page_title = 'All Purchase Orders'
    add_link = reverse_lazy('purchase_order_add')
    add_perms = 'purchaseorder.add_supplier'
    edit_perms = 'purchaseorder.change_purchaseorder'
    edit_url = 'purchase_order_edit'
    view_po = 'purchase_order_display'

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        kwargs.update({
            'edit_perms': self.request.user.has_perm('purchaseorder.change_purchaseorder'),
            'delete_perms': self.request.user.has_perm('purchaseorder.delete_purchaseorder'),
            'view_perms': self.request.user.has_perm('purchaseorder.view_purchaseorder'),
            'detail_url': self.detail_url,
            'edit_url': self.edit_url,
            'delete_url': self.delete_url,
            'view_po': self.view_po,  # Pass view_po here
        })
        return kwargs


class PurchasePaymentCreateByIDView(LoginRequiredMixin, CreateView):
    model = PurchasePayment
    form_class = PurchasePaymentForm
    template_name = 'add_payment.html'  # Adjust to your actual template
    success_url = reverse_lazy('purchase_order_list')

    # Or reverse_lazy('purchase_order_detail') if you want to redirect to a detail page

    def dispatch(self, request, *args, **kwargs):
        """
        Ensure the purchase order has a remaining balance before proceeding.
        """
        self.purchase_order_id = self.kwargs.get('purchase_order_id')
        self.purchase_order = get_object_or_404(PurchaseOrder, pk=self.purchase_order_id)

        # Check if there's any due left
        if self.purchase_order.get_amount_due() <= 0:
            messages.error(request, f"Purchase Order {self.purchase_order_id} is already fully paid.")
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Prepopulate the 'purchase_order' field with the specific purchase order.
        """
        return {'purchase_order': self.purchase_order}

    def get_form_kwargs(self):
        """
        Pass the specific purchase order to the form instance if needed.
        """
        kwargs = super().get_form_kwargs()
        purchase_order = self.kwargs.get('purchase_order_id')
        kwargs['initial'] = {'purchase_order': purchase_order}
        kwargs['purchase_order'] = purchase_order  # Add this line
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_order'] = self.purchase_order
        context['due_amount'] = self.purchase_order.get_amount_due()
        return context

    def form_valid(self, form):
        """
        1. Assign the correct PurchaseOrder to the payment.
        2. Check if the payment amount exceeds the remaining due.
        3. If everything is valid, save the payment and update account balances if applicable.
        """
        form.instance.purchase_order = self.purchase_order

        # Example: Suppose your PurchaseOrder has a get_amount_due() method
        if form.cleaned_data['amount'] > self.purchase_order.get_amount_due():
            form.add_error(
                'amount',
                f"Payment amount cannot exceed the remaining balance of {self.purchase_order.get_amount_due()}."
            )
            return self.form_invalid(form)

        messages.success(self.request, "Payment added successfully!")
        return super().form_valid(form)


from django.views.generic.detail import DetailView


class PurchaseOrderPaymentsModalView(LoginRequiredMixin, DetailView):
    model = PurchaseOrder
    template_name = 'purchase_order_payments_modal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve related payments
        context['payments'] = self.object.purchaseorderpayments.all()
        return context
