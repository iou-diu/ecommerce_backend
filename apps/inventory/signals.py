# inventory/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.ecom.models import StockEntry
from apps.inventory.models import PurchaseOrder, PurchaseOrderItem

@receiver(pre_save, sender=PurchaseOrder)
def purchase_order_status_change(sender, instance, **kwargs):

    print("signal paisi inventory")
    if not instance.pk:
        # The PurchaseOrder is new, so it can't have a status change yet
        return

    # Fetch the previous instance from the database
    try:
        previous = PurchaseOrder.objects.get(pk=instance.pk)
    except PurchaseOrder.DoesNotExist:
        # The PurchaseOrder doesn't exist in the database; perhaps it's new
        return

    # Check if the status has changed to 'delivered'
    if previous.status != 'received' and instance.status == 'received':
        # The status has changed to 'delivered'; process stock entries
        for item in instance.items.all():
            # Create a StockEntry for each item
            StockEntry.objects.create(
                variant=item.variant,
                quantity=item.quantity_ordered,
                change_type='purchase',
                notes=f"Received via Purchase Order {instance.id}"
            )
       
