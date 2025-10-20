from datetime import date
from django.utils.timezone import now

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Case, When, IntegerField, Count
from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from decouple import config

import requests
from django.db.models import Avg, Count, Case, When

from apps.user.models import CustomUser, CustomerUser
from apps.ecom.models import (
    Address, BusinessSetting, CustomerProfile, FlashDeal, ProductVariant, SliderImage, Category,
    Brand, Attribute, AttributeValue, Tag, Product, Cart, Order,
    Payment, Coupon, ShippingMethod, Transaction, Wishlist, WishlistItem, Review,
    ReviewImage, ProductFAQ, Tax, OrderLine, CartItem, ReviewReply
)
from .serializers import (
    AddressSerializer, CustomerProfileSerializer, FlashDealSerializer, OrderCreateSerializer,
    SliderImageSerializer, CategorySerializer, BrandSerializer,
    AttributeSerializer, AttributeValueSerializer, TagSerializer,
    ProductSerializer, CartSerializer, OrderSerializer, PaymentSerializer,
    CouponSerializer, ShippingMethodSerializer, TransactionSerializer, WishlistSerializer,
    WishlistItemSerializer, ReviewSerializer, ReviewImageSerializer,
    ProductFAQSerializer, TaxSerializer, ProductSearchSerializer,
    ProductDetailSerializer, ReviewReplySerializer
)
from api.utils.custom_cart import OrderProcessingService
from rest_framework.exceptions import ValidationError


class CustomerProfileViewSet(viewsets.GenericViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create a profile instance for the authenticated user
        profile, created = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by('-id')
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        'id', 'full_name', 'address_line_1', 'address_line_2', 'city',
        'state_or_province', 'postal_code', 'country', 'phone_number',
        'is_default_shipping', 'is_default_billing', 'address_type'
    ]
    search_fields = ['full_name', 'address_line_1', 'address_line_2', 'city']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(for_product=True).order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['parent', 'is_featured', 'is_active']  # Filter by parent and active status
    search_fields = ['name', 'description', 'meta_title', 'meta_description']  # Enable search on important fields

    def get_queryset(self):
        queryset = Category.objects.filter(for_product=True)

        # Limit recursion depth for children annotations
        is_only_parent = self.request.query_params.get('isonlyparent', '').lower() == 'true'
        if is_only_parent:
            queryset = queryset.annotate(children_count=Count('children')).filter(children_count__gt=0)

        is_popular = self.request.query_params.get('isPopular', '').lower() == 'true'
        if is_popular:
            menu_setting = BusinessSetting.objects.filter(key='menu_categories').first()
            if menu_setting and menu_setting.value:
                try:
                    category_ids = [int(cat_id) for cat_id in menu_setting.value.split(',')]
                    order_case = Case(
                        *[When(id=cat_id, then=pos) for pos, cat_id in enumerate(category_ids)],
                        output_field=IntegerField()
                    )
                    queryset = queryset.filter(id__in=category_ids).annotate(ordering=order_case).order_by('ordering')
                except ValueError:
                    queryset = queryset.none()
            else:
                queryset = queryset.none()

        return queryset.order_by('-id')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Brand.objects.all().order_by('-id')
    serializer_class = BrandSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name', 'description', 'meta_title', 'meta_description', 'slug', 'is_active']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.all().order_by('-id')
    serializer_class = AttributeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name', 'data_type', 'unit', 'is_filterable', 'is_variation']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AttributeValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttributeValue.objects.all().order_by('-id')
    serializer_class = AttributeValueSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'attribute', 'value', 'color_code']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('-id')
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name', 'category', 'brand', 'unit', 'min_order_quantity', 'max_order_quantity',
                        'description', 'meta_title', 'meta_description', 'slug', 'is_active', 'created_at',
                        'updated_at', 'warranty', 'is_variant', 'default_variant']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


from rest_framework.viewsets import ReadOnlyModelViewSet


# class FeaturedProductViewSet(ReadOnlyModelViewSet):
#     queryset = Product.objects.filter(is_featured=True, is_active=True).order_by('-id')
#     serializer_class = ProductSerializer
#     permission_classes = [AllowAny]
class FeaturedProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_featured=True, is_active=True).order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        # Fetch featured products
        featured_products = self.get_queryset()
        # print("Queryset count:", featured_products.count())
        # print("Queryset results:", featured_products)

        # Serialize the products
        serialized_products = self.get_serializer(featured_products, many=True).data
        # print("Serialized products:", serialized_products)

        # Create groups of 4 products
        response_data = []
        group_size = 4
        index = 0

        while index < len(serialized_products):
            group_end = index + group_size
            group_products = serialized_products[index:group_end]

            # Add the group to the response
            response_data.append({
                "type": "group",
                "products": group_products,
            })
            index = group_end

        # Return the response
        return Response(response_data)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user', 'session_key', 'created_at', 'updated_at', 'checked_out']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user', 'shipping_address', 'billing_address', 'shipping_method', 'coupon', 'status',
                        'subtotal', 'shipping_cost', 'total_discount', 'total_amount', 'payment_status', 'created_at',
                        'updated_at', 'notes']
    search_fields = ['name', 'description']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        # For regular users, return only their orders
        return Order.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'order', 'amount', 'provider', 'payment_method', 'status', 'transaction_id', 'created_at',
                        'confirmed_at']
    search_fields = ['name', 'description']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        # For regular users, return only their orders
        return Payment.objects.filter(order__user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all()
        # For regular users, return transactions related to their payments
        return Transaction.objects.filter(payment__order__user=user)


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def validate_coupon(self, request):
        code = request.data.get('code')
        order_amount = request.data.get('order_amount', 0)
        coupon = Coupon.objects.filter(code=code, is_active=True).first()

        if not coupon:
            return Response({'error': 'Invalid or inactive coupon'}, status=400)

        if coupon.expiration_date < date.today():
            return Response({'error': 'Coupon has expired'}, status=400)

        if coupon.max_uses and coupon.used_count >= coupon.max_uses:
            return Response({'error': 'Coupon usage limit reached'}, status=400)

        if order_amount < coupon.minimum_order_amount:
            return Response({'error': 'Minimum order amount not met'}, status=400)

        discount = coupon.discount_value if coupon.discount_type == 'flat' else min(
            (coupon.discount_value / 100) * order_amount,
            coupon.maximum_discount_amount or float('inf')
        )

        return Response({
            'success': 'Coupon is valid',
            'discount': discount,
            'discount_type': coupon.discount_type
        }, status=200)


class ShippingMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShippingMethod.objects.all().order_by('-id')
    serializer_class = ShippingMethodSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name', 'description', 'cost', 'estimated_min_delivery_days',
                        'estimated_max_delivery_days', 'is_active']
    search_fields = ['name', 'description']
    http_method_names = ['get']  # Only allow GET methods

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all().order_by('-id')
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user', 'created_at']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all().order_by('-id')
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'wishlist', 'variant', 'added_at']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'product', 'user', 'rating',
                        'is_approved', 'created_at', 'is_verified_purchase']
    search_fields = ['title', 'comment']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # Get product_id from filter
        product_id = request.query_params.get('product')
        if product_id:
            product_stats = Review.objects.filter(product_id=product_id).aggregate(
                avg_rating=Avg('rating'),
                rating_1=Count(Case(When(rating=1, then=1))),
                rating_2=Count(Case(When(rating=2, then=1))),
                rating_3=Count(Case(When(rating=3, then=1))),
                rating_4=Count(Case(When(rating=4, then=1))),
                rating_5=Count(Case(When(rating=5, then=1)))
            )
            response.data['product_stats'] = product_stats

        return response

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response({'error': list(e)}, status=status.HTTP_400_BAD_REQUEST)


class ReviewImageViewSet(viewsets.ModelViewSet):
    queryset = ReviewImage.objects.all().order_by('-id')
    serializer_class = ReviewImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'review', 'alt_text', 'uploaded_at']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReviewReplyViewSet(viewsets.ModelViewSet):
    queryset = ReviewReply.objects.all().order_by('-id')
    serializer_class = ReviewReplySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'review', 'user']

    def get_permissions(self):
        """Allow anyone to GET, but restrict POST, PUT, DELETE to authenticated users."""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductFAQViewSet(viewsets.ModelViewSet):
    queryset = ProductFAQ.objects.all().order_by('-id')
    serializer_class = ProductFAQSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'product', 'question', 'answer', 'created_at']
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TaxViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tax.objects.all().order_by('-id')
    serializer_class = TaxSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name', 'tax_type', 'is_active']
    search_fields = ['name', ]

    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CheckoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def initiate_checkout(self, request):
        # cart_id = request.data.get("cart_id")
        shipping_address_id = request.data.get("shipping_address_id")
        billing_address_id = request.data.get("billing_address_id")
        shipping_method_id = request.data.get("shipping_method_id")

        # print(self.request.user)

        # return Response("haha", status=status.HTTP_201_CREATED)

        # Validate cart
        cart = Cart.objects.filter(user=request.user, checked_out=False).first()
        # cart = Cart.objects.filter(id=cart_id, user=request.user, checked_out=False).first()
        if not cart:
            return Response({"error": "Invalid cart"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate addresses
        shipping_address = Address.objects.filter(id=shipping_address_id, user=request.user).first()
        billing_address = Address.objects.filter(id=billing_address_id, user=request.user).first()
        if not shipping_address or not billing_address:
            return Response({"error": "Invalid address"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate order totals
        subtotal = sum(item.variant.price * item.quantity for item in cart.items.all())
        shipping_cost = ShippingMethod.objects.get(id=shipping_method_id).cost
        total_amount = subtotal + shipping_cost

        # Create order
        order = Order.objects.create(
            user=request.user.customeruser,
            shipping_address=shipping_address,
            billing_address=billing_address,
            shipping_method_id=shipping_method_id,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total_amount=total_amount,
            payment_status="not_paid",
            status="pending"
        )

        # Add each cart item to OrderLine
        for item in cart.items.all():
            OrderLine.objects.create(
                order=order,
                variant=item.variant,
                product_name=item.variant.product.name,
                sku=item.variant.sku,
                quantity=item.quantity,
                price=item.variant.price,
                total_price=item.variant.price * item.quantity
            )

        # Mark cart as checked out
        cart.checked_out = True
        cart.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def initiate_payment(self, request, pk=None):
        order = get_object_or_404(Order, id=pk, user=request.user, payment_status="not_paid")
        print(order)
        print(order.total_amount)

        store_id = config('store_id')
        store_password = config('store_passwd')
        success_url = config('success_url')
        # ssl_validator_url = config('SSL_VALIDATE_URL')
        payload = {
            'store_id': store_id,
            'store_passwd': store_password,
            'total_amount': order.total_amount,
            'currency': 'BDT',
            'tran_id': f"order_{order.id}",
            'success_url': success_url,
            # 'fail_url': settings.FAIL_URL,
            # 'cancel_url': settings.CANCEL_URL,
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_phone': '876787',
            # 'cus_phone': request.user.phone_number,  # Add this if available
            'cus_add1': '123 Your Address Line',  # Required field
            'cus_city': 'Your City',  # Optional but recommended
            'cus_state': 'Your State',  # Optional
            'cus_postcode': '1234',  # Optional
            'cus_country': 'Bangladesh',  # Optional
            'shipping_method': 'Courier',
            'ship_name': 'COD',
            'ship_add1': 'random',
            'ship_city': 'Dhaka',
            'ship_postcode': '23',
            'ship_country': 'fdfd',
            'product_name': 'hdf',
            'product_category': 'df',
            'product_profile': 'general'
        }

        response = requests.post("https://sandbox.sslcommerz.com/gwprocess/v4/api.php", data=payload)
        print(response.json())
        if response.status_code == 200 and 'GatewayPageURL' in response.json():
            return Response({"payment_url": response.json()['GatewayPageURL']}, status=status.HTTP_200_OK)
        return Response({"error": "Payment initialization failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=True, methods=['get'])
    def verify_payment(self, request, pk=None):
        order = get_object_or_404(Order, id=pk, user=request.user)
        val_id = request.GET.get("val_id")

        if not val_id:
            return Response({"error": "Invalid validation ID"}, status=status.HTTP_400_BAD_REQUEST)

        verify_url = f"{config('SSL_VALIDATE_URL')}?val_id={val_id}&store_id={config('store_id')}&store_passwd={config('store_passwd')}&format=json"
        response = requests.get(verify_url)

        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'VALID':
                order.payment_status = 'paid'
                order.status = 'processing'
                order.save()
                return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)
            order.payment_status = 'failed'
            order.save()
            return Response({"message": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Verification request failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class AvailableProductsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Fetch all active products with available stock.
        """
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# In your views.py


def payment_success(request):
    # Extract val_id from query parameters
    val_id = request.GET.get('val_id')
    tran_id = request.GET.get('tran_id')  # You may also get transaction ID and other details here

    # You could save val_id to your database or log it here
    return JsonResponse({'val_id': val_id, 'tran_id': tran_id})


class ProductSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be searched based on various criteria.
    """
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        'variants__attributes',
        'images',
        'tags',
        'category',
        'brand'
    )
    serializer_class = ProductSearchSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'category__id': ['exact'],
        'category__slug': ['exact'],
        'brand__id': ['exact'],
        'brand__slug': ['exact'],
        'tags__name': ['exact', 'icontains'],
        'variants__price': ['gte', 'lte'],
    }
    search_fields = ['name', 'slug', 'variants__sku', 'description']

    def get_queryset(self):
        queryset = super().get_queryset().distinct()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(variants__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(variants__price__lte=max_price)
        return queryset


# class ProductDetailViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint that provides detailed information about a specific product.
#     """
#     queryset = Product.objects.filter(is_active=True)
#     serializer_class = ProductDetailSerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'slug'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['category', 'brand', 'is_featured', 'is_shop_featured']

class ProductDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that provides detailed information about a specific product.
    Supports OR-based filtering for category and its subcategories.
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug', 'variants__sku', 'description']

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        # Apply category + subcategories OR filter
        category_id = self.request.query_params.get('category')
        if category_id:
            child_ids = Category.objects.filter(parent_id=category_id).values_list('id', flat=True)
            all_ids = list(child_ids) + [int(category_id)]
            queryset = queryset.filter(category_id__in=all_ids)

        # Optional filtering
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand=brand)

        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')

        is_shop_featured = self.request.query_params.get('is_shop_featured')
        if is_shop_featured is not None:
            queryset = queryset.filter(is_shop_featured=is_shop_featured.lower() == 'true')

        return queryset


class CreateOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        if not isinstance(user, CustomerUser) and not isinstance(user, CustomUser):
            return Response({"error": "User is not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Validate shipping and billing address
        shipping_address_id = request.data.get("shipping_address_id")
        billing_address_id = request.data.get("billing_address_id")

        if not Address.objects.filter(user=user, id=shipping_address_id).exists():
            return Response({"error": "Shipping address not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not Address.objects.filter(user=user, id=billing_address_id).exists():
            return Response({"error": "Billing address not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the address objects
        shipping_address = Address.objects.get(id=shipping_address_id)
        billing_address = Address.objects.get(id=billing_address_id)

        # Fetch and validate shipping method
        shipping_method_id = request.data.get("shipping_method_id")
        try:
            shipping_method = ShippingMethod.objects.get(id=shipping_method_id, is_active=True)
        except ShippingMethod.DoesNotExist:
            return Response({"error": "Shipping method not found or inactive."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate shipping cost
        shipping_cost = shipping_method.cost if shipping_method.cost is not None else 0

        # Calculate subtotal and other order values based on products
        products_data = request.data.get('products', [])
        subtotal = 0
        for product in products_data:
            variant_id = product.get('variant_id')
            quantity = product.get('quantity')

            try:
                variant = ProductVariant.objects.get(id=variant_id)
                subtotal += variant.retail_price * quantity
            except ProductVariant.DoesNotExist:
                return Response({"error": f"Product variant with ID {variant_id} does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Handle coupon validation if provided
        coupon_code = request.data.get('coupon_code')
        discount = 0
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if coupon.expiration_date < date.today():
                    return Response({"error": "This coupon has expired."}, status=status.HTTP_400_BAD_REQUEST)

                if coupon.max_uses is not None and coupon.used_count >= coupon.max_uses:
                    return Response({"error": "This coupon has reached its maximum usage limit."},
                                    status=status.HTTP_400_BAD_REQUEST)

                if subtotal < coupon.minimum_order_amount:
                    return Response(
                        {"error": f"Minimum order amount to use this coupon is {coupon.minimum_order_amount}."},
                        status=status.HTTP_400_BAD_REQUEST)

                if coupon.discount_type == 'flat':
                    discount = min(coupon.discount_value, coupon.maximum_discount_amount or coupon.discount_value)
                elif coupon.discount_type == 'percentage':
                    discount = min((coupon.discount_value / 100) * subtotal, coupon.maximum_discount_amount or subtotal)

                coupon.used_count += 1
                coupon.save()
            except Coupon.DoesNotExist:
                return Response({"error": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total amount
        total_amount = subtotal + shipping_cost - discount

        # Create the order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            shipping_method=shipping_method,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total_discount=discount,
            total_amount=total_amount,
            status='pending'
        )

        # Process order lines
        for product in products_data:
            variant = ProductVariant.objects.get(id=product.get('variant_id'))
            quantity = product.get('quantity')
            OrderLine.objects.create(
                order=order,
                variant=variant,
                product_name=variant.product.name,
                sku=variant.sku,
                quantity=quantity,
                price=variant.price,
                total_price=variant.price * quantity
            )

        return Response({
            "message": "Order created successfully",
            "order_id": order.id,
            "status": order.status,
            "subtotal": str(order.subtotal),
            "total_discount": str(discount),
            "total_amount": str(order.total_amount)
        }, status=status.HTTP_201_CREATED)


class SliderImageAPIView(generics.ListAPIView):
    serializer_class = SliderImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return SliderImage.objects.filter(is_active=True).order_by('order', '-created_at')


class OrderAndPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get payment method from request
        payment_method = request.data.get('payment_method')

        # Validate addresses
        shipping_address_id = request.data.get("shipping_address_id")
        billing_address_id = request.data.get("billing_address_id")

        if not hasattr(request.user, 'profile'):
            return Response({"error": "Please update your profile."}, status=status.HTTP_400_BAD_REQUEST)

        if not Address.objects.filter(user=request.user, id=shipping_address_id).exists():
            return Response({"error": "Shipping address not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not Address.objects.filter(user=request.user, id=billing_address_id).exists():
            return Response({"error": "Billing address not found."}, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = Address.objects.get(id=shipping_address_id)
        billing_address = Address.objects.get(id=billing_address_id)

        # Validate shipping method
        shipping_method_id = request.data.get("shipping_method_id")
        try:
            shipping_method = ShippingMethod.objects.get(id=shipping_method_id, is_active=True)
        except ShippingMethod.DoesNotExist:
            return Response({"error": "Invalid shipping method"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate order totals
        products_data = request.data.get('products', [])

        subtotal = 0
        order_lines = []

        for product in products_data:
            variant_id = product.get('variant_id')
            quantity = product.get('quantity')

            try:
                variant = ProductVariant.objects.get(id=variant_id)
                subtotal += variant.retail_price * quantity
                order_lines.append({
                    'variant': variant,
                    'quantity': quantity,
                    'price': variant.retail_price
                })
            except ProductVariant.DoesNotExist:
                return Response(
                    {"error": f"Product variant {variant_id} not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Handle coupon if provided
        coupon_code = request.data.get('coupon_code')
        discount = 0
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if coupon.expiration_date < date.today():
                    return Response({"error": "Coupon expired"}, status=status.HTTP_400_BAD_REQUEST)

                if coupon.max_uses and coupon.used_count >= coupon.max_uses:
                    return Response({"error": "Coupon usage limit reached"}, status=status.HTTP_400_BAD_REQUEST)

                if subtotal < coupon.minimum_order_amount:
                    return Response({"error": f"Minimum order amount: {coupon.minimum_order_amount}"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Calculate discount
                if coupon.discount_type == 'flat':
                    discount = min(coupon.discount_value, coupon.maximum_discount_amount or float('inf'))
                else:  # percentage
                    discount = min((coupon.discount_value / 100) * subtotal,
                                   coupon.maximum_discount_amount or float('inf'))

                coupon.used_count += 1
                coupon.save()
            except Coupon.DoesNotExist:
                return Response({"error": "Invalid coupon"}, status=status.HTTP_400_BAD_REQUEST)

        shipping_cost = shipping_method.cost or 0
        total_amount = subtotal + shipping_cost - discount

        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            shipping_method=shipping_method,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total_discount=discount,
            total_amount=total_amount,
            payment_status="not_paid",
            status="pending"
        )

        # Create order lines
        for line in order_lines:
            OrderLine.objects.create(
                order=order,
                variant=line['variant'],
                product_name=line['variant'].product.name,
                sku=line['variant'].sku,
                quantity=line['quantity'],
                price=line['price'],
                total_price=line['price'] * line['quantity']
            )

        # Handle payment based on method
        if payment_method == 'COD':
            # For Cash on Delivery, just return the order details
            return Response({
                "message": "Order created successfully",
                "order_id": order.id,
                "payment_method": "COD",
                "status": order.status,
                "total_amount": total_amount
            }, status=status.HTTP_201_CREATED)
        else:
            # For online payment, initiate SSL Commerz
            store_id = config('store_id')
            store_password = config('store_passwd')
            success_url = config('success_url')
            # success_url = 'http://localhost:3000'

            payment_payload = {
                'store_id': store_id,
                'store_passwd': store_password,
                'total_amount': order.total_amount,
                'currency': 'BDT',
                'tran_id': f"order_{order.order_uuid}",
                'success_url': success_url + '?order_verify=' + str(order.order_uuid) + '&order_id=' + str(order.id),
                # 'success_url': success_url + '/order_verify' + '?order_verify=' + str(order.order_uuid),
                'fail_url': success_url + '?order_verify=' + str(order.order_uuid) + '&order_id=' + str(order.id),
                'cancel_url': success_url + '?order_verify=' + str(order.order_uuid) + '&order_id=' + str(order.id),
                'cus_name': request.user.username,
                'cus_email': request.user.email,
                'cus_phone': getattr(request.user.profile, 'phone', None),
                # 'cus_phone': request.user.phone_number,  # Add this if available
                'cus_add1': '123 Your Address Line',  # Required field
                'cus_city': 'Your City',  # Optional but recommended
                'cus_state': 'Your State',  # Optional
                'cus_postcode': '1234',  # Optional
                'cus_country': 'Bangladesh',  # Optional
                'shipping_method': 'Courier',
                'ship_name': 'COD',
                'ship_add1': 'random',
                'ship_city': 'Dhaka',
                'ship_postcode': '23',
                'ship_country': 'fdfd',
                'product_name': 'hdf',
                'product_category': 'df',
                'product_profile': 'general'
            }

            response = requests.post(
                "https://sandbox.sslcommerz.com/gwprocess/v4/api.php",
                data=payment_payload
            )

            order.sslcommerz_session_key = response.json()['sessionkey']
            order.save()
            carts = Cart.objects.filter(user=request.user, checked_out=False).update(checked_out=True)

            if response.status_code == 200 and 'GatewayPageURL' in response.json():
                return Response({
                    "message": "Payment initiated",
                    "order_id": order.id,
                    "payment_method": payment_method,
                    "payment_url": response.json()['GatewayPageURL']
                }, status=status.HTTP_200_OK)

            return Response(
                {"error": "Payment initialization failed"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def get(self, request):
        """Handle payment verification"""

        tran_id = request.GET.get("tran_id")

        if not tran_id:
            return Response(
                {"error": "Missing  transaction UUID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract order ID from tran_id
        try:

            order = get_object_or_404(Order, order_uuid=tran_id, user=request.user)
        except (IndexError, ValueError):
            return Response(
                {"error": "Invalid transaction ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify payment with SSL Commerz
        # IS_SSL_SANDBOX = config('IS_SSL_SANDBOX')
        #
        # if IS_SSL_SANDBOX == True:
        #     root_url = 'sandbox'
        # else:
        #     root_url = 'securepay'
        root_url = 'securepay'
        url = "https://" + root_url + ".sslcommerz.com/validator/api/merchantTransIDvalidationAPI.php?store_id=" + config(
            'store_id') + "&store_passwd=" + config(
            'store_passwd') + "&sessionkey=" + order.sslcommerz_session_key + "&format=json"
        response = requests.request("GET", url)

        payment_status = response.json()['status']

        message = payment_status

        if (order is not None and order.payment_status == 'not_paid' and payment_status == 'VALID'):
            order.payment_status = 'paid'
            order.status = 'processing'
            order.order_details = response.json()
            order.save()


        elif order is not None and order.payment_status == 'not_paid' and payment_status == 'FAILED':
            order.payment_status = 'failed'
            order.save()


        else:

            message = 'Already Submitted'

        result = {
            "message": message,
            "order": OrderSerializer(order).data

        }

        return Response(result, status=status.HTTP_201_CREATED)

        verify_url = (
            f"{config('SSL_VALIDATE_URL')}?"
            f"sessionkey={order.sslcommerz_session_key}&"
            f"store_id={config('store_id')}&"
            f"store_passwd={config('store_passwd')}&"
            f"format=json"
        )

        response = requests.get(verify_url)

        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'VALID':
                order.payment_status = 'paid'
                order.status = 'processing'
                order.save()
                return Response({
                    "message": "Payment verified successfully",
                    "order_id": order.id,
                    "status": order.status
                }, status=status.HTTP_200_OK)

            order.payment_status = 'failed'
            order.save()
            return Response({
                "message": "Payment verification failed"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "error": "Verification request failed"
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle payment verification"""
        # payment_method = request.data.get('payment_method')
        tran_id = request.GET.get("tran_id")

        if not tran_id:
            return Response(
                {"error": "Missing  transaction UUID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract order ID from tran_id
        try:

            order = get_object_or_404(Order, order_uuid=tran_id, user=request.user)
        except (IndexError, ValueError):
            return Response(
                {"error": "Invalid transaction ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify payment with SSL Commerz
        IS_SSL_SANDBOX = config('IS_SSL_SANDBOX')

        if IS_SSL_SANDBOX == True:
            root_url = 'sandbox'
        else:
            root_url = 'securepay'
        url = "https://" + root_url + ".sslcommerz.com/validator/api/merchantTransIDvalidationAPI.php?store_id=" + config(
            'store_id') + "&store_passwd=" + config(
            'store_passwd') + "&sessionkey=" + order.sslcommerz_session_key + "&format=json"

        response = requests.request("GET", url)
        payment_status = response.json()['status']
        message = payment_status

        if (order is not None and order.payment_status == 'not_paid' and payment_status == 'VALID'):
            order.payment_status = 'paid'
            order.status = 'processing'
            order.order_details = response.json()
            order.save()


        elif order is not None and order.payment_status == 'not_paid' and payment_status == 'FAILED':
            order.payment_status = 'failed'
            order.save()


        else:

            message = 'Already Submitted'

        result = {
            "message": message,
            "order": OrderSerializer(order).data

        }

        return Response(result, status=status.HTTP_201_CREATED)

        verify_url = (
            f"{config('SSL_VALIDATE_URL')}?"
            f"sessionkey={order.sslcommerz_session_key}&"
            f"store_id={config('store_id')}&"
            f"store_passwd={config('store_passwd')}&"
            f"format=json"
        )

        response = requests.get(verify_url)

        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'VALID':
                order.payment_status = 'paid'
                order.status = 'processing'
                order.save()
                return Response({
                    "message": "Payment verified successfully",
                    "order_id": order.id,
                    "status": order.status
                }, status=status.HTTP_200_OK)

            order.payment_status = 'failed'
            order.save()
            return Response({
                "message": "Payment verification failed"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "error": "Verification request failed"
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


###### Flash Deal

class FlashDealViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlashDeal.objects.all()
    permission_classes = [AllowAny]
    serializer_class = FlashDealSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']  # Filter by active status
    search_fields = ['title', 'description']  # Search by title or description
    ordering_fields = ['start_date', 'end_date', 'created_at']  # Ordering options

    def get_queryset(self):
        """
        Optionally filter FlashDeals based on whether they are live.
        Add 'live' as a query parameter (?live=true) to get only live deals.
        """
        queryset = super().get_queryset()
        live = self.request.query_params.get('live')
        if live and live.lower() == 'true':
            queryset = queryset.filter(
                start_date__lte=now(), end_date__gte=now(), is_active=True
            )
        return queryset


# class NewArrivalAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Fetch all active products ordered by creation date
#         new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')

#         # Serialize the products using the existing ProductSerializer
#         serialized_products = ProductSerializer(new_arrivals, many=True).data

#         # Create the alternating structure for the response
#         response_data = []
#         group_size = 5  # Initial group size
#         index = 0

#         while index < len(serialized_products):
#             # Add a group
#             group_end = index + group_size
#             group_products = serialized_products[index:group_end]
#             if group_products:  # Only add if group has products
#                 response_data.append({
#                     "type": "group",
#                     "products": group_products,
#                 })
#             index = group_end

#             # Add a single product
#             if index < len(serialized_products):
#                 response_data.append({
#                     "type": "single",
#                     "product": serialized_products[index],
#                 })
#                 index += 1

#             # Alternate group size between 5 and 6
#             group_size = 6 if group_size == 5 else 5

#         return Response(response_data)

class NewArrivalAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Fetch all active products ordered by creation date
        new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')

        # Serialize the products using the existing ProductSerializer
        serialized_products = ProductSerializer(new_arrivals, many=True).data

        # Create the alternating structure for the response
        response_data = []
        group_size = 5  # Initial group size
        index = 0

        while index < len(serialized_products):
            # Add a group if there are enough products for the group
            if len(serialized_products) - index >= group_size:
                group_end = index + group_size
                group_products = serialized_products[index:group_end]
                response_data.append({
                    "type": "group",
                    "products": group_products,
                })
                index = group_end
            else:
                # Not enough products for a group, stop processing
                break

            # Add a single product if there's at least one product remaining
            if index < len(serialized_products):
                response_data.append({
                    "type": "single",
                    "product": serialized_products[index],
                })
                index += 1
            else:
                # No more products to process
                break

            # Alternate group size between 5 and 6
            group_size = 6 if group_size == 5 else 5

        return Response(response_data)
