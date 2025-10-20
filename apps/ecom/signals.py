from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.ecom.models import Product, ProductVariant, StockEntry, Payment, Order
from apps.mailersend_utils import send_mailersend_email
from django.template.loader import render_to_string


@receiver(post_save, sender=StockEntry)
def update_stock_quantity_on_save(sender, instance, created, **kwargs):
    if created:
        signed_quantity = instance.get_signed_quantity()
        instance.variant.stock_quantity += signed_quantity
        instance.variant.save()


# Signal to create a default variant
@receiver(post_save, sender=Product)
def create_default_variant(sender, instance, created, **kwargs):
    if created and not instance.is_variant and not instance.default_variant:
        variant = ProductVariant.objects.create(
            product=instance,
            sku=f"{instance.slug}-default",
            price=0.00,
            stock_quantity=0,
        )
        instance.default_variant = variant
        instance.save()


@receiver(post_save, sender=Payment)
def send_invoice_on_payment_completed(sender, instance, created, **kwargs):
    # Only send invoice if status changed to 'completed'
    if instance.status == 'completed':
        # Check if status just changed to completed (not just saved again)
        if hasattr(instance, '_previous_status'):
            if instance._previous_status != 'completed':
                order = instance.order
                user = order.user
                if user and user.email:
                    subject = f"Your Invoice for Order #{order.id}"
                    to_list = [user.email]
                    context = {
                        "order": order,
                        "payment": instance,
                        "user": user,
                    }

                    send_mailersend_email(
                        to_list=to_list,
                        subject=subject,
                        body_or_template="invoice.html",
                        context=context,
                        is_template=True
                    )
        else:
            # If _previous_status not set, fallback: send only if just created and status is completed
            if created:
                order = instance.order
                user = order.user
                if user and user.email:
                    subject = f"Your Invoice for Order #{order.id}"
                    to_list = [user.email]
                    context = {
                        "order": order,
                        "payment": instance,
                        "user": user,
                    }
                    send_mailersend_email(
                        to_list=to_list,
                        subject=subject,
                        body_or_template="invoice.html",
                        context=context,
                        is_template=True
                    )


@receiver(post_save, sender=Order)
def send_invoice_on_order_paid(sender, instance, created, **kwargs):
    # Only send invoice if payment_status changed to 'paid'
    if instance.payment_status == 'paid':
        if hasattr(instance, '_previous_payment_status'):
            if instance._previous_payment_status != 'paid':
                user = instance.user
                if user and user.email:
                    subject = "Order Paid"
                    to_list = [user.email]
                    context = {
                        "order": instance,
                        "user": user,
                    }
                    send_mailersend_email(
                        to_list=to_list,
                        subject=subject,
                        body_or_template="invoice.html",
                        context=context,
                        is_template=True
                    )
        else:
            # If _previous_payment_status not set, fallback: send only if just created and status is paid
            if created:
                user = instance.user
                if user and user.email:
                    subject = "Order Paid"
                    to_list = [user.email]
                    context = {
                        "order": instance,
                        "payment": instance.payments.filter(status='completed').last(),
                        "user": user,
                    }
                    send_mailersend_email(
                        to_list=to_list,
                        subject=subject,
                        body_or_template="invoice.html",
                        context=context,
                        is_template=True
                    )


# Add a pre_save signal to track previous status
@receiver(pre_save, sender=Payment)
def track_previous_payment_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Payment.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except Payment.DoesNotExist:
            instance._previous_status = None


@receiver(pre_save, sender=Order)
def track_previous_order_payment_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Order.objects.get(pk=instance.pk)
            instance._previous_payment_status = previous.payment_status
        except Order.DoesNotExist:
            instance._previous_payment_status = None
