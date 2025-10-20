# models.py
import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import string

from django.db.models import SET_NULL
from django.utils.text import slugify
from apps.user.models import CustomUser, CustomerUser
from decimal import Decimal


class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user}"


# Address model to store multiple addresses for a user
class Address(models.Model):
    ADDRESS_TYPE = [
        ('home', 'Home'),
        ('office', 'Office'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses', null=True,
                             blank=True)  # Associated user
    full_name = models.CharField(max_length=255)  # Full name for the address
    address_line_1 = models.CharField(max_length=255)  # Primary address line
    address_line_2 = models.CharField(max_length=255, blank=True)  # Secondary address line
    city = models.CharField(max_length=255)  # City name
    state_or_province = models.CharField(max_length=255)  # State or province name
    postal_code = models.CharField(max_length=20)  # Postal code
    country = models.CharField(max_length=100, default='Bangladesh')  # Country name
    phone_number = models.CharField(max_length=20)  # Contact phone number
    is_default_shipping = models.BooleanField(default=False)  # Default shipping address flag
    is_default_billing = models.BooleanField(default=False)  # Default billing address flag
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE, default='home')

    def __str__(self):
        return f"{self.full_name} - {self.address_line_1}, {self.city}, {self.country}"


# Category model for organizing products hierarchically
class Category(models.Model):
    name = models.CharField(max_length=255)  # Category name
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children')  # Parent category
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Category image
    icon = models.ImageField(upload_to='category_icon/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Category description
    meta_title = models.CharField(max_length=255, null=True, blank=True)  # SEO meta title
    meta_description = models.TextField(null=True, blank=True)  # SEO meta description
    slug = models.SlugField(unique=True)  # URL-friendly slug
    is_active = models.BooleanField(default=True)  # Active status flag
    is_featured = models.BooleanField(default=False)  # Active status flag

    for_solution = models.BooleanField(default=False)
    for_product = models.BooleanField(default=True)  # If the category is for products

    def __str__(self):
        return self.name


# Brand model representing product brands
class Brand(models.Model):
    name = models.CharField(max_length=255)  # Brand name
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True)  # Brand logo image
    description = models.TextField(null=True, blank=True)  # Brand description
    meta_title = models.CharField(max_length=255, null=True, blank=True)  # SEO meta title
    meta_description = models.TextField(null=True, blank=True)  # SEO meta description
    slug = models.SlugField(unique=True)  # URL-friendly slug
    is_active = models.BooleanField(default=True)  # Active status flag

    def __str__(self):
        return self.name


# Attribute model for defining product attributes
class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Attribute name
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    data_type = models.CharField(max_length=50, choices=(
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
    ))  # Type of data
    unit = models.CharField(max_length=50, null=True, blank=True)  # Unit of measure
    is_filterable = models.BooleanField(default=False)  # If attribute is used for filtering
    is_variation = models.BooleanField(default=False)  # If attribute is used for product variations

    def __str__(self):
        return str(self.name)


# AttributeValue model for possible values of an attribute
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')  # Associated attribute
    value = models.CharField(max_length=255)  # Value of the attribute
    color_code = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f"{self.value} ({self.attribute.name})"


# class AttributeValueParentChildMapping(models.Model):
#     parent_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='allowed_child_mappings')
#     child_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='allowed_parent_mappings')

#     class Meta:
#         unique_together = ('parent_value', 'child_value')

# Tag model for product tagging
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Tag name

    def __str__(self):
        return self.name


# Product model for storing product information
class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('lb', 'Pound'),
        ('oz', 'Ounce'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Pieces'),
        ('m', 'Meter'),
        ('cm', 'Centimeter'),
        ('mm', 'Millimeter'),
        ('ft', 'Feet'),
        ('in', 'Inch'),
    ]

    name = models.CharField(max_length=512)  # Product name

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='products')  # Associated category
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)  # Associated brand
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, null=True,
                            blank=True)  # Unit of measure  # Unit of measure
    min_order_quantity = models.PositiveIntegerField(default=1)  # Minimum order quantity
    max_order_quantity = models.PositiveIntegerField(default=100)  # Maximum order quantity
    tags = models.ManyToManyField(Tag, blank=True)  # Associated tags
    description = models.TextField()  # Product description
    key_features = models.TextField(default='', blank=True)  # Product Key Features
    meta_title = models.CharField(max_length=255, null=True, blank=True)  # SEO meta title
    meta_description = models.TextField(null=True, blank=True)  # SEO meta description
    slug = models.SlugField(max_length=600, unique=True)  # URL-friendly slug
    is_active = models.BooleanField(default=True)  # Active status flag
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    warranty = models.CharField(max_length=255, null=True, blank=True)  # Warranty information
    is_variant = models.BooleanField(default=False)  # Whether a product is variant or not
    is_featured = models.BooleanField(default=False)  # Featured product flag
    default_variant = models.OneToOneField('ProductVariant', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='default_for_product')  # Default variant reference

    is_saleable = models.BooleanField(default=True)  # If the product is on sale

    is_shop_featured = models.BooleanField(default=False)  # If the product is featured in the shop

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate slug if not already provided
        if not self.slug:
            try:
                slug_base = slugify(self.name)
                unique_suffix = ''.join(random.choices(string.digits, k=4))  # Generate a 4-digit random number
                self.slug = f"{slug_base}-{unique_suffix}"
            except:
                unique_suffix = ''.join(random.choices(string.digits, k=8))
                self.slug = f"{unique_suffix}"
        if self.is_shop_featured:
            # Ensure only one product can be featured in the shop
            Product.objects.filter(is_shop_featured=True).update(is_shop_featured=False)
        super().save(*args, **kwargs)  # Call the parent save method


# ProductImage model for storing product images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # Associated product
    image = models.ImageField(upload_to='product_images/')  # Image file
    alt_text = models.CharField(max_length=255, null=True, blank=True)  # Alternative text for the image
    is_featured = models.BooleanField(default=False)  # Featured image flag
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp

    def __str__(self):
        return f"Image for {self.product.name} - {self.alt_text}"


# ProductAttribute model linking attributes to products
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_attributes')  # Associated product
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)  # Associated attribute
    values = models.ManyToManyField(AttributeValue)  # Possible values for the attribute

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"


# ProductVariant model representing product variations
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')  # Base product
    sku = models.CharField(max_length=200, unique=True)  # Stock Keeping Unit
    upc = models.CharField(max_length=24, unique=True, null=True, blank=True)  # Universal Product Code
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Buying Price')  # Current price
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                       blank=True, verbose_name='Selling Price')  # Original price before discount
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      default=0.0)  # Offer price (if any)
    offer_start_time = models.DateTimeField(null=True, blank=True)  # Start time of the offer
    offer_end_time = models.DateTimeField(null=True, blank=True)  # End time of the offer
    is_active = models.BooleanField(default=True)  # Active status flag
    attributes = models.ManyToManyField(AttributeValue, related_name='variants',
                                        blank=True)  # Attribute values defining the variant
    image = models.ImageField(upload_to='variant_images/', null=True, blank=True)  # Variant-specific image
    stock_quantity = models.IntegerField(default=0)  # Quantity in stock

    def calculate_retail_price(self):
        """
        Calculate retail price dynamically based on the offer price or base price.
        """
        if self.offer_price and self.offer_price > 0:
            return self.offer_price
        return self.price

    def __str__(self):
        return f"{self.product.name} - {self.sku}"


# StockEntry model for stock change history
class StockEntry(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_entries')
    quantity = models.PositiveIntegerField()  # Ensure quantity is always positive
    CHANGE_TYPE_CHOICES = (
        ('purchase', 'Purchase'),  # Increases stock
        ('sale', 'Sale'),  # Decreases stock
        ('return', 'Return'),  # Increases stock
        ('adjustment', 'Adjustment'),  # Can increase or decrease stock
    )
    change_type = models.CharField(max_length=50, choices=CHANGE_TYPE_CHOICES)
    adjustment_direction = models.CharField(
        max_length=10,
        choices=(
            ('increase', 'Increase'),
            ('decrease', 'Decrease'),
        ),
        null=True,  # Only required when change_type is 'adjustment'
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', null=True, blank=True)

    def __str__(self):
        return f"{self.change_type} of {self.quantity} for {self.variant.sku}"

    def get_signed_quantity(self):
        if self.change_type in ['purchase', 'return']:
            return self.quantity  # Positive quantity increases stock
        elif self.change_type == 'sale':
            return -self.quantity  # Negative quantity decreases stock
        elif self.change_type == 'adjustment':
            if self.adjustment_direction == 'increase':
                return self.quantity
            elif self.adjustment_direction == 'decrease':
                return -self.quantity
            else:
                raise ValueError("Adjustment direction must be specified for adjustments.")
        else:
            return 0


# Commented out Warehouse-related models for future use

# # Warehouse model representing physical warehouses or stores
# class Warehouse(models.Model):
#     name = models.CharField(max_length=255)  # Warehouse name
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)  # Warehouse address
#     is_store = models.BooleanField(default=False)  # If the warehouse is also a store
#     is_active = models.BooleanField(default=True)  # Active status flag

#     def __str__(self):
#         return self.name

# # ProductVariantStock model to manage stock per warehouse
# class ProductVariantStock(models.Model):
#     variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_levels')  # Associated variant
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_levels')  # Associated warehouse
#     quantity = models.IntegerField(default=0)  # Quantity in stock
#     safety_stock = models.IntegerField(default=0)  # Safety stock threshold
#     is_tracked = models.BooleanField(default=True)  # If stock is actively tracked

#     class Meta:
#         unique_together = ('variant', 'warehouse')  # Ensure unique variant-warehouse combination

#     def __str__(self):
#         return f"Stock for {self.variant.sku} in {self.warehouse.name}"

# # StockTransfer model for transferring stock between warehouses
# class StockTransfer(models.Model):
#     reference_number = models.CharField(max_length=100, unique=True)  # Unique transfer identifier
#     from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='outgoing_transfers')  # Source warehouse
#     to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='incoming_transfers')  # Destination warehouse
#     created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
#     status = models.CharField(max_length=50, choices=(
#         ('pending', 'Pending'),
#         ('in_transit', 'In Transit'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     ), default='pending')  # Transfer status
#     notes = models.TextField(null=True, blank=True)  # Additional notes

#     def __str__(self):
#         return f"Transfer {self.reference_number} from {self.from_warehouse.name} to {self.to_warehouse.name}"

# # StockTransferItem model for items in a stock transfer
# class StockTransferItem(models.Model):
#     transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='items')  # Associated stock transfer
#     variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)  # Variant being transferred
#     quantity = models.PositiveIntegerField()  # Quantity being transferred

#     def __str__(self):
#         return f"{self.quantity} of {self.variant.sku} in transfer {self.transfer.reference_number}"

# Cart model for user shopping carts
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
                             blank=True)  # Associated user (nullable for guests)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Session key for anonymous users
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    checked_out = models.BooleanField(default=False)  # If the cart has been converted to an order

    # def __str__(self):
    #     return f"Cart {self.id} for user {self.user}"


# CartItem model for items in a cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='items')  # this is not use in new system
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)  # Variant added to the cart
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the variant
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when item was added

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
                             blank=True, related_name='user_cart_items')  # Associated user (nullable for guests)

    def save(self, *args, **kwargs):
        if not self.cart:
            cart = Cart.objects.filter(checked_out=False, user=self.user)
            if cart:
                self.cart = cart[0]
            else:
                cart = Cart.objects.create(user=self.user)
                self.cart = cart
        super().save(*args, **kwargs)  # Call the parent save method


# Order model for customer orders
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # Ordering user
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True,
                                         related_name='shipping_orders')  # Shipping address
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True,
                                        related_name='billing_orders')  # Billing address
    shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.SET_NULL,
                                        null=True)  # Chosen shipping method
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)  # Applied coupon
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ), default='pending')  # Order status
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Subtotal amount
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Shipping cost
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total discount amount
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total payable amount
    payment_status = models.CharField(max_length=50, choices=(
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ), default='not_paid')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Order creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    notes = models.TextField(null=True, blank=True)  # Additional order notes

    order_uuid = models.UUIDField(
        unique=False,
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True
    )  # Unique UUID for the order
    order_details = models.JSONField(
        null=True,
        blank=True
    )  # Store additional order details
    sslcommerz_session_key = models.TextField(
        null=True,
        blank=True
    )  # Session
    paid_date = models.DateTimeField(null=True, blank=True)  # Date when the order was paid

    def save(self, *args, **kwargs):
        if not self.paid_date:
            if self.payment_status == 'paid':
                from django.utils import timezone
                self.paid_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


# OrderLine model for items in an order
class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')  # Associated order
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)  # Purchased variant
    product_name = models.CharField(max_length=255)  # Product name at time of purchase
    sku = models.CharField(max_length=255)  # SKU at time of purchase
    quantity = models.PositiveIntegerField()  # Quantity purchased

    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit without offer original
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # original price - offer price 
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))  # Price after discount
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=Decimal('0.0'))  # Total price (final_price * quantity)

    # Removed warehouse field since Warehouse model is not used
    def save(self, *args, **kwargs):
        # Automatically calculate discount, final_price, and total_price
        if not self.discount:
            self.discount = self.price - (self.variant.offer_price or self.price)
        if not self.final_price:
            self.final_price = self.price - self.discount
        if not self.total_price:
            self.total_price = self.final_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product_name} in order {self.order.id}"


# Payment model for order payments
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')  # Associated order
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    provider = models.CharField(max_length=255)  # Payment provider (e.g., Stripe, PayPal)
    payment_method = models.CharField(max_length=50, null=True, blank=True)  # Payment method (e.g., Credit Card)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ), default='pending')  # Payment status
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  # Transaction identifier
    created_at = models.DateTimeField(auto_now_add=True)  # Payment creation timestamp
    confirmed_at = models.DateTimeField(null=True, blank=True)  # Payment confirmation timestamp

    def __str__(self):
        return f"Payment {self.id} - {self.status} for order {self.order.id}"


# PaymentMethod model for available payment methods
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)  # Payment method name
    provider = models.CharField(max_length=100)  # Payment provider name
    is_active = models.BooleanField(default=True)  # Active status flag
    config = models.JSONField(null=True, blank=True)  # Configuration settings

    def __str__(self):
        return self.name


# Transaction model for payment transactions
class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')  # Associated payment
    status = models.CharField(max_length=50)  # Transaction status
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    transaction_id = models.CharField(max_length=255)  # Transaction identifier
    timestamp = models.DateTimeField(auto_now_add=True)  # Transaction timestamp
    response = models.JSONField(null=True, blank=True)  # Response data from payment gateway

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"


# Coupon model for discount coupons
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Unique coupon code
    discount_type = models.CharField(max_length=50,
                                     choices=(('flat', 'Flat'), ('percentage', 'Percentage')))  # Discount type
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)  # Discount value
    maximum_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                               default=0.0)  # Minimum order amount to apply coupon
    expiration_date = models.DateField()  # Expiration date of the coupon
    max_uses = models.PositiveIntegerField(null=True, blank=True)  # Maximum number of uses
    used_count = models.PositiveIntegerField(default=0)  # Times the coupon has been used
    is_active = models.BooleanField(default=True)  # Active status flag

    def __str__(self):
        return f"Coupon {self.code}"


# ShippingMethod model for available shipping options
class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)  # Shipping method name
    description = models.TextField(null=True, blank=True)  # Shipping method description
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Shipping cost
    estimated_min_delivery_days = models.IntegerField()  # Minimum estimated delivery time
    estimated_max_delivery_days = models.IntegerField()  # Maximum estimated delivery time
    is_active = models.BooleanField(default=True)  # Active status flag

    def __str__(self):
        return self.name


# Wishlist model for user wishlists
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlists')  # Associated user
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp

    def __str__(self):
        return f"Wishlist {self.id} for user {self.user}"


# WishlistItem model for items in a wishlist
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')  # Associated wishlist
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)  # Variant added to the wishlist
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when item was added

    def __str__(self):
        return f"Wishlist item {self.variant.sku} in wishlist {self.wishlist.id}"


# Review model for product reviews
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(default=5)
    title = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified_purchase = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.user} for {self.product.name}"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for review {self.review.id}"


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_reply')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    reply = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply for review {self.review.id}"


# Notification model for user notifications
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Notified user
    message = models.TextField()  # Notification message
    notification_type = models.CharField(max_length=50, choices=(
        ('order_update', 'Order Update'),
        ('promotion', 'Promotion'),
        ('system', 'System'),
    ))  # Type of notification
    read = models.BooleanField(default=False)  # Read status flag
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"


# LoyaltyPoint model for user loyalty points
class LoyaltyPoint(models.Model):
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)  # Associated user
    points = models.PositiveIntegerField(default=0)  # Loyalty points balance
    last_updated = models.DateTimeField(auto_now=True)  # Last update timestamp

    def __str__(self):
        return f"Loyalty points for {self.user} - {self.points}"


# ProductFAQ model for frequently asked questions about a product
class ProductFAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='faqs')  # Associated product
    question = models.CharField(max_length=255)  # FAQ question
    answer = models.TextField()  # FAQ answer
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp

    def __str__(self):
        return f"FAQ for {self.product.name}"


# Tax model for tax configurations
class Tax(models.Model):
    FLAT = 'flat'
    PERCENTAGE = 'percentage'
    TAX_TYPE_CHOICES = [
        (FLAT, 'Flat'),
        (PERCENTAGE, 'Percentage'),
    ]

    name = models.CharField(max_length=100)  # Tax name
    value = models.DecimalField(max_digits=5, decimal_places=2)  # Tax percentage or flat amount
    tax_type = models.CharField(max_length=10, choices=TAX_TYPE_CHOICES,
                                default=PERCENTAGE)  # Tax type: flat or percentage
    is_active = models.BooleanField(default=True)  # Active status flag

    def __str__(self):
        return f"Tax {self.name} - {self.value} ({self.get_tax_type_display()})"


# class SupportTicket(models.Model):
#     TICKET_STATUS_CHOICES = [
#         ('open', 'Open'),
#         ('in_progress', 'In Progress'),
#         ('resolved', 'Resolved'),
#         ('closed', 'Closed'),
#     ]

#     ticket_id = models.CharField(max_length=12, unique=True, editable=False, null=True)
#     name = models.CharField(max_length=100)
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
#     description = models.TextField(blank=True, null=True)
#     solution = models.TextField(blank=True, null=True)
#     attachment = models.FileField(upload_to='support_attachments/', blank=True, null=True)
#     status = models.CharField(max_length=15, choices=TICKET_STATUS_CHOICES, default='open')
#     priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)  # Save initially to get the ID
#         if not self.ticket_id:
#             self.ticket_id = f"TKT{str(self.id).zfill(8)}"
#             self.save(update_fields=['ticket_id'])  # Save again to update ticket_id with a valid ID

#     def __str__(self):
#         return f"Ticket #{self.ticket_id} - {self.name}"

class SupportTicket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    TICKET_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    TICKET_CATEGORY_CHOICES = [
        ('general', 'General Support'),
        ('billing', 'Billing'),
        ('technical', 'Technical Support'),
        ('other', 'Other'),
    ]

    ticket_id = models.CharField(max_length=12, unique=True, editable=False, null=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_tickets")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="assigned_tickets")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=20, choices=TICKET_CATEGORY_CHOICES, default='general')

    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='support_attachments/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=TICKET_STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=TICKET_PRIORITY_CHOICES, default='medium')
    is_closed = models.BooleanField(default=False)  # Marks if the ticket is closed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate ticket ID if it doesn't already exist
        super().save(*args, **kwargs)
        if not self.ticket_id:
            self.ticket_id = f"TKT{str(self.id).zfill(8)}"
            self.save(update_fields=['ticket_id'])

    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.name}"


class SupportTicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # User or Admin sending the message
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender} on Ticket {self.ticket.ticket_id}"


class FavoriteProductVariant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_variants')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_variant')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product_variant.sku}"


class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/', help_text='Upload slider image')
    alt_text = models.CharField(max_length=255, help_text='Alternative text for image')
    url = models.URLField(max_length=500, help_text='URL for the slider link')
    title = models.CharField(max_length=255, blank=True, null=True, help_text='Optional title for the slider')
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text='Optional subtitle for the slider')
    order = models.IntegerField(default=0, help_text='Order of appearance')
    is_active = models.BooleanField(default=True, help_text='Toggle slider visibility')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Slider Image'
        verbose_name_plural = 'Slider Images'

    def __str__(self):
        return f"Slider - {self.title if self.title else self.alt_text}"

    def save(self, *args, **kwargs):
        # For new records, set order to the next highest value if not specified
        if not self.pk and not self.order:
            last_order = SliderImage.objects.all().aggregate(models.Max('order'))['order__max']
            self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)


class BusinessSetting(models.Model):
    key = models.CharField(max_length=255, unique=True)  # Unique key for the setting
    value = models.JSONField(null=True, blank=True)  # Stores value as JSON (flexible for various use cases)
    description = models.TextField(null=True, blank=True)  # Optional description for the setting

    def __str__(self):
        return self.key


# Flash Deal 
import json


class FlashDeal(models.Model):
    title = models.CharField(max_length=255)  # Title of the flash deal
    description = models.TextField(blank=True, null=True)  # Optional description
    banner_image = models.ImageField(upload_to='flash_deals/', blank=True, null=True)  # Banner image
    start_date = models.DateTimeField()  # Start date and time of the deal
    end_date = models.DateTimeField()  # End date and time of the deal
    product_variants = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)  # Active status flag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_live(self):
        """Check if the deal is currently live."""
        from django.utils.timezone import now
        return self.start_date <= now() <= self.end_date and self.is_active

    def get_variants(self):
        """Fetch associated ProductVariant objects."""
        variant_data = json.loads(self.product_variants or "[]")
        variant_ids = [entry['id'] for entry in variant_data]
        return ProductVariant.objects.filter(id__in=variant_ids, is_active=True)
