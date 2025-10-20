from django.test import TestCase
from rest_framework.test import APIClient
from apps.ecom.models import Cart, Address, ShippingMethod, Order  # Import relevant models for setup
from apps.user.models import CustomerUser  # Import CustomerUser directly

class EcomAPITest(TestCase):
    def setUp(self):
        # Create a CustomerUser instance for the tests
        self.user = CustomerUser.objects.create_user(
            email="testuser@example.com",
            password="password",
            name="Test User"
        )
        
        # Authenticate the test client as the CustomerUser
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Setup required data for checkout and payment, including required fields
        self.shipping_method = ShippingMethod.objects.create(
            name="Home Delivery",
            cost=60.0,
            estimated_min_delivery_days=1,  # Required field
            estimated_max_delivery_days=3   # Required field
        )
        self.address = Address.objects.create(
            user=self.user,
            full_name="Test User",
            city="Dhaka",
            state_or_province="Dhaka"
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_shipping_options(self):
        response = self.client.get("/api/v1/ecom/shipping/")
        self.assertEqual(response.status_code, 200)
        print("Shipping Options Response:", response.json())

    def test_checkout(self):
        data = {
            "cart_id": self.cart.id,
            "shipping_address_id": self.address.id,
            "billing_address_id": self.address.id,
            "shipping_method_id": self.shipping_method.id,
        }
        response = self.client.post("/api/v1/ecom/checkout/initiate_checkout/", data, format='json')
        self.assertEqual(response.status_code, 201)
        print("Checkout Response:", response.json())

    def test_payment(self):
        # Create an order as setup for payment
        order = Order.objects.create(
            user=self.user,
            shipping_address=self.address,
            billing_address=self.address,
            shipping_method=self.shipping_method,
            total_amount=100.0,
            payment_status="not_paid",
            status="pending"
        )
        response = self.client.post(f"/api/v1/ecom/payment/initiate_payment/{order.id}/")
        self.assertEqual(response.status_code, 200)
        print("Payment Initiation Response:", response.json())
