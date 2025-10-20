from django.urls import reverse
import django_tables2 as tables
from django_tables2 import Column
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.helpers import CustomTable

from .models import PO, PurchaseOrder, Requisition, Supplier
class RequisitionTable(tables.Table):
    items = Column(verbose_name="Items", orderable=False, empty_values=())
    approve = Column(verbose_name="Action", orderable=False, empty_values=())

    class Meta:
        model = Requisition
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'requested_by', 'created_at', 'approved', 'approved_by', 'notes', 'items', 'approve')
        empty_text = 'No requisitions available'
        orderable = True

    def render_items(self, record):
        # Same render_items method as before
        items = record.items.all()
        if not items.exists():
            return mark_safe("<p>No items</p>")
        
        table_html = """
        <table class="table table-sm table-bordered">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
        """

        for item in items:
            table_html += f"<tr><td>{item.variant}</td><td>{item.quantity}</td></tr>"

        table_html += "</tbody></table>"
        return mark_safe(table_html)

    def render_approve(self, record):
        """
        Render the "Approve" button if the requisition is not yet approved.
        """
        if record.approved:
            return format_html('<span class="badge badge-success">Already Approved</span>')
        else:
            approve_url = reverse('approve_requisition', args=[record.id])
            return format_html('<a href="{}" class="btn btn-success btn-sm">Approve</a>', approve_url)

# class RequisitionTable(tables.Table):
#     items = Column(verbose_name="Items", orderable=False, empty_values=())

#     class Meta:
#         model = Requisition
#         template_name = 'django_tables2/bootstrap4.html'
#         fields = ('id', 'requested_by', 'created_at', 'approved', 'approved_by', 'notes', 'items')
#         empty_text = 'No requisitions available'
#         orderable = True

#     def render_items(self, record):
#         """
#         Render the items as an HTML table with 'Item' and 'Quantity' headers.
#         """
#         items = record.items.all()  # Get the related items for this requisition
#         if not items.exists():
#             return mark_safe("<p>No items</p>")
        
#         # Create table with headers "Item" and "Quantity"
#         table_html = """
#         <table class="table table-sm table-bordered">
#             <thead>
#                 <tr>
#                     <th>Item</th>
#                     <th>Quantity</th>
#                 </tr>
#             </thead>
#             <tbody>
#         """

#         for item in items:
#             table_html += f"<tr><td>{item.variant}</td><td>{item.quantity}</td></tr>"

#         table_html += "</tbody></table>"

#         return mark_safe(table_html)

#     def render_approved(self, value):
#         """
#         Show a label for approved status.
#         """
#         if value:
#             return format_html('<span class="badge badge-success">Approved</span>')
#         else:
#             return format_html('<span class="badge badge-warning">Pending</span>')




class SupplierTable(CustomTable):
    edit_url = 'supplier_update'
    delete_url = 'supplier_delete'

    class Meta:
        model = Supplier
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'contact_person', 'phone_number', 'email', 'address', 'contact_type')
        empty_text = 'No suppliers available'
        orderable = True


class PurchaseOrderTable(CustomTable):
    action = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')
    edit_url = 'purchase_order_update'
    delete_url = 'purchase_order_delete'
    view_po = 'purchase_order_display'

    class Meta:
        model = PurchaseOrder
        template_name = 'django_tables2/bootstrap4.html'
        fields = [
            'requisition', 'supplier', 'order_date', 'expected_delivery_date', 
            'status', 'global_discount_type', 'global_discount_value', 
            'shipping_cost', 'purchase_tax_name', 'final_total_cost'
        ]
        empty_text = 'No purchase orders available'
        orderable = True

    
    def render_action(self, record):
        """
        Render custom action buttons for the Expense table.
        """
        url = []
        details_url = reverse('purchase_order_payments_modal', args=[record.pk])
        details_button = f'<button type="button" class="btn btn-sm btn-light-info my-1" onclick="loadModal(\'{details_url}\')"><i class="flaticon-eye"></i> View Payments</button>'

        if  self.view_po:
            print("pooooooooo")
            view_po = reverse(self.view_po, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-danger"><i class="flaticon-eye"></i></a>' % view_po)
        if self.edit_perms and self.edit_url:
            edit_url = reverse(self.edit_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-warning my-1"><i class="flaticon-edit"></i> Edit</a>' % edit_url)


   
        add_payment_url = reverse('purchase_payment_add_by_id', args=[record.pk])
        add_payment_button = f'<a href="{add_payment_url}" class="btn btn-sm btn-light-success py-1"><i class="flaticon-add"></i> Add Payment</a>'


        return mark_safe(f" {details_button} {add_payment_button} {' '.join(url)}")


class POTable(CustomTable):
    # edit_url = 'purchase_order_update'
    delete_url = 'purchase_order_delete'
    view_po = 'purchase_order_display'

    class Meta:
        model = PO
        template_name = 'django_tables2/bootstrap4.html'
        fields = [
            'requisition', 'supplier', 'order_date', 'expected_delivery_date', 
            'status', 'global_discount_type', 'global_discount_value', 
            'shipping_cost', 'purchase_tax_name', 'final_total_cost'
        ]
        empty_text = 'No purchase orders available'
        orderable = True