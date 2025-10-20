import apps.user.models
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

import random
from apps.ecom.models import ShippingMethod, Address, Cart, CartItem, Order, ProductVariant
from apps.user.models import CustomerUser
from django.contrib.auth.hashers import make_password
import string


class OrderProcessingService:
    def __init__(self, data):
        self.data = data
        self.cart = None
        self.order = None
        self.user = None
        self.shipping_address = None
        self.billing_address = None
        self.shipping_method = None

    def validate_data(self):
        required_fields = [
            "email",
            "name",
            "shipping_address",
            "billing_address",
            "shipping_method_id",
            "products",
        ]

        missing_fields = [field for field in required_fields if field not in self.data]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        if not self.data["products"]:
            raise ValidationError("No products provided")

        try:
            self.shipping_method = ShippingMethod.objects.get(
                id=self.data["shipping_method_id"], is_active=True
            )
        except ShippingMethod.DoesNotExist:
            raise ValidationError("Invalid or inactive shipping method")

        for product in self.data["products"]:
            if "varient_id" not in product or "quantity" not in product:
                raise ValidationError("Each product must have varient_id and quantity")

    def random_password(self):
        return f"{random.randint(100000, 999999)}_{string.ascii_letters}"

    def get_or_create_user(self):
        User = get_user_model()
        email = self.data["email"]
        name = self.data["name"]

        try:
            self.user = CustomerUser.objects.get(email=email)
        except CustomerUser.DoesNotExist:
            self.user = CustomerUser.objects.create(
                email=email, name=name, is_active=True, password=make_password(self.random_password())
            )
        return self.user

    def create_addresses(self):
        shipping_data = self.data["shipping_address"]
        shipping_data["user"] = self.user
        self.shipping_address = Address.objects.create(**shipping_data)

        billing_data = self.data["billing_address"]
        billing_data["user"] = self.user
        self.billing_address = Address.objects.create(**billing_data)

        return self.shipping_address, self.billing_address

    def create_cart(self):
        self.cart = Cart.objects.create(user=self.user)

        for product in self.data["products"]:
            try:
                variant = ProductVariant.objects.get(id=product["varient_id"])
                CartItem.objects.create(
                    cart=self.cart, variant=variant, quantity=product["quantity"]
                )
            except ProductVariant.DoesNotExist:
                raise ValidationError(
                    f"Product variant with id {product['varient_id']} not found"
                )

        return self.cart

    def calculate_totals(self):
        subtotal = Decimal("0.0")
        for item in self.cart.items.all():
            subtotal += item.variant.price * item.quantity

        shipping_cost = self.shipping_method.cost
        total_discount = Decimal("0.0")
        total_amount = subtotal + shipping_cost - total_discount

        return {
            "subtotal": subtotal,
            "shipping_cost": shipping_cost,
            "total_discount": total_discount,
            "total_amount": total_amount,
        }

    @transaction.atomic
    def process_order(self):
        try:
            self.validate_data()

            self.get_or_create_user()

            self.create_addresses()

            self.create_cart()

            totals = self.calculate_totals()

            self.order = Order.objects.create(
                user=self.user,
                shipping_address=self.shipping_address,
                billing_address=self.billing_address,
                shipping_method=self.shipping_method,
                subtotal=totals["subtotal"],
                shipping_cost=totals["shipping_cost"],
                total_discount=totals["total_discount"],
                total_amount=totals["total_amount"],
                status="pending",
                payment_status="not_paid",
            )

            self.cart.checked_out = True
            self.cart.save()

            return self.order

        except Exception as e:
            raise ValidationError(str(e))