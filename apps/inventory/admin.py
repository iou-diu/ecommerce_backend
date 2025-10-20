from django.contrib import admin



from django.contrib import admin
from .models import PO, POAdditionalCost, POItem, PurchasePayment, Supplier, Requisition, PurchaseOrder, GoodsReceivedNote,RequisitionItem,PurchaseOrderItem,GoodsReceivedItem, TestProduct, TestStockLine

admin.site.register(Supplier)
admin.site.register(Requisition)
admin.site.register(RequisitionItem)

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        'requisition', 'supplier', 'order_date', 'purchase_tax_value',
        'additional_cost_total', 'final_total_cost',
        'total_paid', 'total_due'
    ]
    list_filter = ['status', 'order_date', 'expected_delivery_date']
    search_fields = ['requisition__id', 'supplier__name', 'purchase_tax_name']
    ordering = ['-order_date']
    readonly_fields = ['order_date']

    def total_paid(self, obj):
        """Show the total of all completed payments."""
        return obj.get_amount_paid()
    total_paid.short_description = "Total Paid"

    def total_due(self, obj):
        """Show the remaining amount to be paid."""
        return obj.get_amount_due()
    total_due.short_description = "Total Due"



class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order','variant','quantity_ordered','price_per_unit','discount','tax','line_total')
admin.site.register(PurchaseOrderItem,PurchaseOrderItemAdmin)
admin.site.register(GoodsReceivedNote)
admin.site.register(GoodsReceivedItem)

admin.site.register(TestProduct)
admin.site.register(TestStockLine)


admin.site.register(PO)
admin.site.register(POAdditionalCost)
admin.site.register(POItem)

admin.site.register(PurchasePayment)