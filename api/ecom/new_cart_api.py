from django.contrib.auth import get_user_model
from psycopg2._psycopg import Decimal
from psycopg2.errorcodes import INVALID_GRANT_OPERATION
from rest_framework import viewsets, serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count

from apps.ecom.models import ProductVariant, CartItem
from apps.user.models import CustomUser


# Serializers
# class ProductVariantSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='product.name', read_only=True)
#
#     class Meta:
#         model = ProductVariant
#         fields = ['id', 'name', 'sku', 'price', 'offer_price', 'image', 'stock_quantity']
#
#
# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['id', 'variant', 'quantity', 'added_at']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#
#         variant_data = ProductVariantSerializer(instance.variant).data  # This returns a dictionary
#         representation['name'] = variant_data.get('name')
#         representation['sku'] = variant_data.get('sku')
#         price = variant_data.get('price')
#         representation['price'] = variant_data.get('price')
#         representation['offer_price'] = variant_data.get('offer_price')
#         offer_price = variant_data.get('offer_price')
#         representation['image'] = variant_data.get('image')  # Already a string from the serializer
#         representation['stock_quantity'] = variant_data.get('stock_quantity')
#
#         representation['is_offer'] = True if 0 < float(offer_price) < float(price) else False
#
#         return representation

class ProductVariantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)
    retail_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'name',
            'sku',
            'upc',
            'price',
            'retail_price',
            'offer_price',
            'offer_start_time',
            'offer_end_time',
            'image',
            'stock_quantity',
            'is_active',
        ]

    def get_retail_price(self, obj):
        try:
            return obj.calculate_retail_price()
        except Exception:
            return obj.price


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'quantity', 'added_at']

    def to_representation(self, instance):
        from django.utils import timezone

        representation = super().to_representation(instance)
        v = instance.variant

        # Variant details
        representation['name'] = getattr(v.product, 'name', None)
        representation['sku'] = v.sku
        # Use retail_price if available, else price
        base_price = getattr(v, 'retail_price', None)
        if base_price is None:
            base_price = v.price
        representation['price'] = base_price
        representation['retail_price'] = base_price
        representation['offer_price'] = v.offer_price
        representation['image'] = v.image.url if getattr(v, 'image', None) else None
        representation['stock_quantity'] = v.stock_quantity

        # Offer status considering offer window
        now = timezone.now()
        window_ok = True
        if v.offer_start_time and now < v.offer_start_time:
            window_ok = False
        if v.offer_end_time and now > v.offer_end_time:
            window_ok = False

        offer_price = v.offer_price or 0
        try:
            representation['is_offer'] = bool(
                window_ok and float(offer_price) > 0 and float(offer_price) < float(base_price)
            )
        except Exception:
            representation['is_offer'] = False

        return representation


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'quantity']

    def validate(self, attrs):
        # Perform stock validation only when creating or updating the quantity
        if 'variant' in attrs and 'quantity' in attrs:
            variant = attrs['variant']
            quantity = attrs['quantity']
            if variant.stock_quantity < quantity:
                raise serializers.ValidationError("Not enough stock available.")
        return attrs

    def update(self, instance, validated_data):
        # Allow updating only the quantity, without requiring the variant
        if 'variant' in validated_data:
            instance.variant = validated_data['variant']
        if 'quantity' in validated_data:
            instance.quantity = validated_data['quantity']
        instance.save()
        return instance


# Viewset

class MyCartPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        user = self.request.user
        cart_items = CartItem.objects.filter(cart__checked_out=False, user=user)
        total_item = cart_items.count()
        total_price = 0
        total_offer_price = 0

        for item in cart_items:
            variant = item.variant
            price = getattr(variant, 'retail_price', variant.price)
            offer_price = variant.offer_price or 0
            total_price += price * item.quantity
            total_offer_price += offer_price * item.quantity

        total_price = round(total_price, 2)
        total_offer_price = round(total_offer_price, 2)

        return Response(
            {
                "total_item": total_item,
                "total_price": total_price,
                "total_offer_price": total_offer_price,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )



class MyCartViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.filter(cart__checked_out=False).order_by('-added_at')
    serializer_class = CartItemSerializer
    pagination_class = MyCartPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CartItemCreateSerializer
        return CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__checked_out=False, user=user)

    def perform_create(self, serializer):
        variant = serializer.validated_data['variant']
        quantity = serializer.validated_data['quantity']
        user = self.request.user

        # Check if the cart item for the same variant and user already exists
        existing_cart_item = CartItem.objects.filter(cart__checked_out=False, user=user, variant=variant).first()

        if existing_cart_item:
            # Update the quantity of the existing cart item
            new_quantity = existing_cart_item.quantity + quantity

            # Validate stock
            if variant.stock_quantity < quantity:
                raise serializers.ValidationError({
                    "quantity": [
                        "Not enough stock available. Ensure the requested quantity does not exceed available stock."
                    ]
                })

            existing_cart_item.quantity = new_quantity
            existing_cart_item.save()
        else:
            # Deduct stock when adding a new item to the cart
            if variant.stock_quantity < quantity:
                raise serializers.ValidationError({
                    "quantity": [
                        "Not enough stock available. Ensure the requested quantity does not exceed available stock."
                    ]
                })

            variant.stock_quantity -= quantity
            variant.save()
            serializer.save(user=user)

    def perform_update(self, serializer):
        cart_item = self.get_object()
        variant = serializer.validated_data['variant']
        new_quantity = serializer.validated_data['quantity']
        quantity_difference = new_quantity - cart_item.quantity

        if variant.stock_quantity < quantity_difference:
            raise serializers.ValidationError("Not enough stock available.")

        # Adjust stock
        variant.stock_quantity -= quantity_difference
        variant.save()
        serializer.save()

    def perform_destroy(self, instance):
        # Return stock when an item is removed from the cart
        variant = instance.variant
        variant.stock_quantity += instance.quantity
        variant.save()
        instance.delete()
