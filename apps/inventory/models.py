from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.accounting.models import PaymentAccount
from apps.ecom.models import ProductVariant, Tax

User = get_user_model()


# class Supplier(models.Model):
#     name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255, null=True, blank=True)
#     phone_number = models.CharField(max_length=20, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     image = models.ImageField(upload_to='supplier_images/', null=True, blank=True)
#     trade_license_image  = models.ImageField(upload_to='supplier_images/', null=True, blank=True)
#     tin_image  = models.ImageField(upload_to='supplier_images/', null=True, blank=True)
#     def __str__(self):
#         return self.name

class Supplier(models.Model):
    INDIVIDUAL = 'Individual'
    BUSINESS = 'Business'
    CONTACT_TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (BUSINESS, 'Business'),
    ]
    address = models.TextField(null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)  # Name or business name
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default=BUSINESS)
    contact_id = models.CharField(max_length=50, null=True, blank=True)  # Auto-generated or manual
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    alternate_contact_number = models.CharField(max_length=20, null=True, blank=True)
    landline = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    tax_number = models.CharField(max_length=50, null=True, blank=True)

    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pay_term_value = models.PositiveIntegerField(null=True, blank=True)  # Term value (e.g., 1)
    pay_term_unit = models.CharField(
        max_length=10,
        choices=[('Days', 'Days'), ('Months', 'Months')],
        null=True,
        blank=True,
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Address fields
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)

    # Custom fields
    custom_field_1 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_2 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_3 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_4 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_5 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_6 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_7 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_8 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_9 = models.CharField(max_length=255, null=True, blank=True)
    custom_field_10 = models.CharField(max_length=255, null=True, blank=True)

    # Additional fields for image, trade license, and TIN
    image = models.ImageField(upload_to='supplier_images/', null=True, blank=True)
    trade_license = models.FileField(upload_to='supplier_trade_licenses/', null=True, blank=True)
    tin_certificate = models.FileField(upload_to='supplier_tin_certificates/', null=True, blank=True)

    # Shipping Address (if required separately)
    shipping_address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100, null=True, blank=True)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, null=True, blank=True)
    shipping_zip_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Requisition(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_requisitions')
    notes = models.TextField(null=True, blank=True)

    def item_summary(self):
        """
        Returns a comma-separated string of items with quantity and variant names.
        """
        return ", ".join([f"{item.quantity} of {item.variant}" for item in self.items.all()])

    def __str__(self):
        return f"Requisition {self.id} by {self.requested_by}"


class RequisitionItem(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.variant} in requisition {self.requisition.id}"


# PO only for tracking
class PO(models.Model):
    # requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE,related_name='po')
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='po')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=(

        ('ordered', 'Ordered'),
        ('partial', 'Partial'),
        ('completed', 'Completed'),
    ), default='ordered')
    notes = models.TextField(null=True, blank=True)
    global_discount_type = models.CharField(max_length=20, choices=(('percentage', 'Percentage'), ('flat', 'Flat')),
                                            default='percentage')
    global_discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_info = models.TextField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    purchase_tax_name = models.CharField(max_length=50, null=True, blank=True)
    purchase_tax_type = models.CharField(max_length=20, choices=(('percentage', 'Percentage'), ('flat', 'Flat')),
                                         null=True, blank=True)
    purchase_tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    additional_cost_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_total_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    payload = models.JSONField(null=True, blank=True, default=list)
    paymentDays = models.TextField(null=True, blank=True)
    paymentMonths = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.id} for Requisition {self.requisition.id}"


class POAdditionalCost(models.Model):
    purchase_order = models.ForeignKey(PO, on_delete=models.CASCADE, related_name='po_additional_costs')
    description = models.CharField(max_length=100)  # Description of the additional cost
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount} for PO {self.purchase_order.id}"


class POItem(models.Model):
    purchase_order = models.ForeignKey(PO, on_delete=models.CASCADE, related_name='po_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_model = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    line_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity_ordered} of {self.variant} in PO {self.purchase_order.id}"


# PO Ends 

class PurchaseOrder(models.Model):
    requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE, related_name='purchase_order')
    purchase_order = models.OneToOneField(PO, on_delete=models.CASCADE, related_name='po_purchase', null=True,
                                          blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=(
        ('draft', 'Draft'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ), default='ordered')
    notes = models.TextField(null=True, blank=True)
    global_discount_type = models.CharField(max_length=20, choices=(('percentage', 'Percentage'), ('flat', 'Flat')),
                                            default='percentage')
    global_discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_info = models.TextField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    purchase_tax_name = models.CharField(max_length=50, null=True, blank=True)
    purchase_tax_type = models.CharField(max_length=20, choices=(('percentage', 'Percentage'), ('flat', 'Flat')),
                                         null=True, blank=True)
    purchase_tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    additional_cost_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_total_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    payload = models.JSONField(null=True, blank=True, default=list)
    paymentDays = models.TextField(null=True, blank=True)
    paymentMonths = models.TextField(null=True, blank=True)

    def get_amount_paid(self):
        completed_payments = self.purchaseorderpayments.filter(status='completed')
        return sum(payment.amount for payment in completed_payments)

    def get_amount_due(self):
        return (self.final_total_cost or 0) - self.get_amount_paid()

    def __str__(self):
        return f"Add Purchase {self.id} for Requisition {self.requisition.id}"


class AdditionalCost(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='additional_costs')
    description = models.CharField(max_length=100)  # Description of the additional cost
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount} for PO {self.purchase_order.id}"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))  # per-item discount
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # per-item tax
    tax_model = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    line_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # calculated total

    profit_margin_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    expected_selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    selling_tax_model = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='selling_tax')

    def __str__(self):
        return f"{self.quantity_ordered} of {self.variant} in PO {self.purchase_order.id}"


class PurchasePayment(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='purchaseorderpayments')
    payment_account = models.ForeignKey(PaymentAccount, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=(('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')),
        default='pending'
    )
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    document = models.FileField(upload_to="purchaseorder/documents/", blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} for PO {self.purchase_order.id}"


class GoodsReceivedNote(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    received_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"GRN for PO {self.purchase_order.id}"


class GoodsReceivedItem(models.Model):
    goods_received_note = models.ForeignKey(GoodsReceivedNote, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity_received = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity_received} of {self.variant} in GRN {self.goods_received_note.id}"


# Test Models
class TestProduct(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TestStockLine(models.Model):
    product = models.ForeignKey(TestProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
