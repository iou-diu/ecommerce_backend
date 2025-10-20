from django.forms import ValidationError
from rest_framework import serializers

from apps.ecom.models import (
    CustomerProfile,
    FlashDeal,
    OrderLine,
    Product,
    ProductVariant,
    ProductImage,
    Category,
    Brand,
    SliderImage,
    SupportTicket,
    SupportTicketMessage,
    Tag,
    AttributeValue,
    Attribute,
    ProductAttribute,
    Address,
    Transaction, ReviewReply,
)
from apps.user.models import CustomUser, CustomerUser
from django.core.exceptions import ObjectDoesNotExist


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'phone']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False}
        }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'full_name', 'address_line_1', 'address_line_2',
            'city', 'state_or_province', 'postal_code', 'country',
            'phone_number', 'is_default_shipping', 'is_default_billing',
            'address_type'
        ]


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'image', 'icon', 'parent', 'description',
            'meta_title', 'meta_description', 'slug',
            'is_active', 'children'
        ]

    def get_children(self, obj):
        # Limit recursion depth using the context
        depth = self.context.get('depth', 0)
        max_depth = self.context.get('max_depth', 2)  # Default max depth

        if depth >= max_depth:
            return []  # Stop recursion when max depth is reached

        # Pass incremented depth in context for child serializers
        return CategorySerializer(
            obj.children.all(),
            many=True,
            context={'depth': depth + 1, 'max_depth': max_depth}
        ).data


class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'description', 'meta_title', 'meta_description', 'slug', 'is_active']

    def get_logo(self, obj):
        # Return only the file path for the logo field
        if obj.logo:
            return obj.logo.url  # Returns the relative file path
        return None


class AttributeSerializer2(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        read_only=True
    )
    children = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'parent_id', 'children']

    def get_children(self, obj):
        return AttributeSerializer2(obj.children, many=True).data


class SimpleAttributeSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'parent_id']
        # No 'children' field here!


#
# class AttributeValueSerializer2(serializers.ModelSerializer):
#     attribute = SimpleAttributeSerializer(read_only=True)
#
#     class Meta:
#         model = AttributeValue
#         fields = ['id', 'value', 'color_code', 'attribute']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'data_type', 'unit', 'is_filterable', 'is_variation']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')

    class Meta:
        model = AttributeValue
        fields = ['id', 'value', 'color_code', 'attribute_name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['retail_price', 'offer_price']


class ProductSerializer(serializers.ModelSerializer):
    price_details = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'is_saleable', 'price_details', 'category', 'category_name', 'brand', 'brand_name', 'unit',
                  'min_order_quantity', 'max_order_quantity', 'description', 'meta_title', 'meta_description', 'slug',
                  'is_active', 'created_at', 'updated_at', 'warranty', 'is_variant', 'default_variant', 'images']

    def to_representation(self, instance):
        # Start with the default representation
        representation = super().to_representation(instance)
        try:
            # Attempt to fetch the last ProductVariant for the product
            p = ProductVariant.objects.filter(product=instance.id).last()
            # If a variant exists, add price details
            if p:
                representation['retail_price'] = p.retail_price
                representation['offer_price'] = p.offer_price
            else:
                # If no variant exists, set prices to None
                representation['retail_price'] = None
                representation['offer_price'] = None
        except Exception as e:
            # Handle any unexpected exceptions
            representation['retail_price'] = None
            representation['offer_price'] = None
            # Optionally log the exception for debugging
            # logging.error(f"Error fetching ProductVariant for Product {instance.id}: {e}")

        return representation

    def get_images(self, obj):
        items = ProductImage.objects.filter(product=obj.pk)
        data = ProductImageSerializer(items, many=True)
        return data.data

    def get_price_details(self, obj):
        items = ProductVariant.objects.filter(product=obj.pk)
        data = ProductPriceSerializer(items, many=True)
        return data.data


from apps.ecom.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'created_at', 'updated_at', 'checked_out']


class ProductVariantNestedAttributesSerializer(serializers.ModelSerializer):
    # We won't use 'attributes' = ManyToMany => Instead, we'll do a manual grouping
    # attribute_summery = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    filter_id = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'filter_id', 'sku', 'retail_price', 'offer_price',
            'is_active', 'stock_quantity', 'attributes', 'image', 'product'
        ]

    # def get_attribute_summery(self, obj):
    #     return ", ".join(str(attr.value) for attr in obj.attributes.all())

    def get_filter_id(self, obj):
        return obj.id
        # return ", ".join(str(attr.value) for attr in obj.attributes.all())

    def get_attributes(self, obj):
        """
        Gather all AttributeValue objects for this variant
        and build a nested JSON structure:
          - top-level attributeValue (where attribute.parent is None)
          - children are attributeValues whose parent= top-level attribute
        """
        all_values = obj.attributes.all()

        top_level_values = [av for av in all_values if av.attribute.parent is None]

        # We'll build a list of dictionaries
        result = []
        for parent_av in top_level_values:
            parent_dict = {
                "id": parent_av.attribute.id,
                "filter_id": obj.id,
                "name": parent_av.attribute.name,
                "value": parent_av.value,
                "color_code": parent_av.color_code,
                "parent_id": parent_av.attribute.parent_id,
            }

            result.append(parent_dict)

        return result


from apps.ecom.models import Order


class OrderSerializer(serializers.ModelSerializer):
    shipping_mehtod_details = serializers.SerializerMethodField()
    shipping_address_details = serializers.SerializerMethodField()
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_address', 'shipping_address_details', 'billing_address', 'shipping_method',
                  'shipping_mehtod_details', 'coupon', 'status', 'subtotal', 'shipping_cost', 'total_discount',
                  'total_amount', 'payment_status', 'created_at', 'updated_at', 'notes', 'product_details']

    def get_shipping_mehtod_details(self, obj):
        data = {
            'name': obj.shipping_method.name,
            'description': obj.shipping_method.description,
            'cost': obj.shipping_method.cost,
            'estimated_min_delivery_days': obj.shipping_method.estimated_min_delivery_days,
            'estimated_max_delivery_days': obj.shipping_method.estimated_max_delivery_days,
        }

        return data

    def get_shipping_address_details(self, obj):
        address = getattr(obj, 'shipping_address', None)
        if not address:
            return {
                'full_name': '',
                'address_line_1': '',
                'address_line_2': '',
                'city': '',
                'state_or_province': '',
                'postal_code': '',
                'country': '',
                'phone_number': '',
            }

        return {
            'full_name': address.full_name or '',
            'address_line_1': address.address_line_1 or '',
            'address_line_2': address.address_line_2 or '',
            'city': address.city or '',
            'state_or_province': address.state_or_province or '',
            'postal_code': address.postal_code or '',
            'country': address.country or '',
            'phone_number': address.phone_number or '',
        }

    def get_product_details(self, obj):
        data = []
        for item in obj.order_lines.all():
            product_image = item.variant.product.images.first()
            data.append({
                'product_name': item.product_name,
                'sku': item.sku,
                'quantity': item.quantity,
                'price': item.price,
                'total_price': item.total_price,
                'product_image': product_image.image.url if product_image else None
            })

        return data


from apps.ecom.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'provider', 'payment_method', 'status', 'transaction_id', 'created_at',
                  'confirmed_at']


from apps.ecom.models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'maximum_discount_amount', 'minimum_order_amount',
                  'expiration_date', 'max_uses', 'used_count', 'is_active']


from apps.ecom.models import ShippingMethod


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description', 'cost', 'estimated_min_delivery_days', 'estimated_max_delivery_days',
                  'is_active']


from apps.ecom.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'created_at']


from apps.ecom.models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'wishlist', 'variant', 'added_at']


from apps.ecom.models import Review

from apps.ecom.models import ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'review', 'alt_text', 'uploaded_at', 'image']


class ReviewReplySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_profile_picture = serializers.CharField(source='user.profile_picture.url', read_only=True)

    class Meta:
        model = ReviewReply
        fields = ['id', 'review', 'user', 'user_name', 'user_profile_picture', 'image', 'reply', 'uploaded_at']
        read_only_fields = ['user', ]


class ReviewSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_profile_picture = serializers.CharField(source='user.profile_picture.url', read_only=True)
    no_of_reply = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'title', 'no_of_reply',
                  'comment', 'is_approved', 'created_at',
                  'is_verified_purchase', 'images', 'uploaded_images', 'user', 'user_name', 'user_profile_picture']
        read_only_fields = ['is_approved', 'is_verified_purchase']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return value

    def get_no_of_reply(self, obj):
        return obj.review_reply.all().count()

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])

        validated_data['user'] = self.context['request'].user

        try:
            # Check user actually purchased the product
            order_exist = Order.objects.filter(
                user=validated_data['user'],
                order_lines__variant__product=validated_data['product'],
                payment_status='paid'
            )
            if not order_exist.exists():
                validated_data['is_verified_purchase'] = False
            else:
                validated_data['is_verified_purchase'] = True
            review = Review.objects.create(**validated_data)

            # Create ReviewImage instances for each uploaded image
            for image in uploaded_images:
                ReviewImage.objects.create(review=review, image=image)

            return review

        except ObjectDoesNotExist:
            raise ValidationError("You must purchase the product to leave a review.")
        except Exception as e:
            raise ValidationError(
                f"An error occurred while creating the review. Please try again - {str(e)}."
            )


from apps.ecom.models import ProductFAQ


class ProductFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = ['id', 'product', 'question', 'answer', 'created_at']


from apps.ecom.models import Tax


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'name', 'value', 'tax_type', 'is_active']


# this is ecom
class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'sku', 'retail_price', 'offer_price', 'is_active',
            'stock_quantity', 'attributes', 'image', 'product'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_featured']


class ProductSearchSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'is_saleable', 'slug', 'category', 'brand', 'description',
            'is_active', 'variants', 'images', 'tags'
        ]


class ProductAttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)
    attribute = serializers.CharField(source='attribute.name')

    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'values']


class ProductDetailSerializer(serializers.ModelSerializer):
    attributes_summary = serializers.SerializerMethodField()
    variants = ProductVariantNestedAttributesSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    product_attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_attributes_summary(self, instance):
        """
        Create a summary of attributes grouped by name and value,
        with combined filter_ids for identical attributes.
        """
        # Ensure the instance is a Product
        if not hasattr(instance, "variants"):
            raise AttributeError("The instance passed must be a Product object.")

        # Get all related variants
        variants = instance.variants.all()

        # Dictionary to store grouped attributes
        attribute_summary = {}

        for variant in variants:
            for attr_value in variant.attributes.all():  # Loop through attribute values
                attr_name = attr_value.attribute.name
                attr_value_data = {
                    "name": attr_name,
                    "value": attr_value.value,
                    "color_code": attr_value.color_code,
                }

                # Group by attribute name and value
                key = (attr_name, attr_value.value, attr_value.color_code)
                if key not in attribute_summary:
                    attribute_summary[key] = {
                        **attr_value_data,
                        "filter_id": []
                    }

                # Add the variant ID to the filter_id list
                attribute_summary[key]["filter_id"].append(variant.id)

        # Format the response
        grouped_attributes = {}
        for (attr_name, _, _), data in attribute_summary.items():
            if attr_name not in grouped_attributes:
                grouped_attributes[attr_name] = []
            grouped_attributes[attr_name].append(data)

        return grouped_attributes

    # def get_attributes_summary(self, instance):
    #     # Serialize variants data
    #     variants = ProductVariantNestedAttributesSerializer(instance.variants, many=True).data
    #
    #     # Process attributes
    #     attribute_data = {}
    #     for variant in variants:
    #         for attribute in variant.get("attributes", []):
    #             name = attribute.get("name")
    #             value = attribute.get("value")
    #             if name and value:  # Ensure both name and value exist
    #                 if name not in attribute_data:
    #                     attribute_data[name] = set()
    #                 attribute_data[name].add(value)
    #
    #     # Convert Sets to Lists for Readable Output
    #     attribute_data = {k: list(v) for k, v in attribute_data.items()}
    #     return attribute_data


class AddressSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user', 'is_default_shipping', 'is_default_billing')


class ProductItemSerializer(serializers.Serializer):
    varient_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    shipping_address = serializers.IntegerField()
    billing_address_id = serializers.IntegerField()
    shipping_method_id = serializers.IntegerField()
    products = serializers.ListField(
        child=serializers.DictField()
    )

    def validate_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with the provided ID does not exist.")

    def validate_shipping_method(self, shipping_method_id):
        try:
            return ShippingMethod.objects.get(id=shipping_method_id)
        except ShippingMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid shipping method.")

    def create(self, validated_data):
        user_id = validated_data['user_id']
        user = self.validate_user(user_id)

        # Retrieve or create addresses
        shipping_address = Address.objects.get(id=validated_data['shipping_address'])
        billing_address = Address.objects.get(id=validated_data['billing_address_id'])

        # Calculate subtotal from products
        subtotal = self.calculate_subtotal(validated_data['products'])

        # Create the order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            shipping_method_id=validated_data.get('shipping_method_id'),
            subtotal=subtotal,
            shipping_cost=validated_data.get('shipping_cost'),
            total_discount=validated_data.get('total_discount', 0),
            total_amount=subtotal - validated_data.get('total_discount', 0) + validated_data.get('shipping_cost', 0),
            payment_status='not_paid',
            status='pending'
        )

        # Add products to the order as OrderLines
        for product_data in validated_data['products']:
            variant_id = product_data.get('variant_id')
            quantity = product_data.get('quantity')

            variant = ProductVariant.objects.get(id=variant_id)
            OrderLine.objects.create(
                order=order,
                variant=variant,
                product_name=variant.product.name,
                sku=variant.sku,
                quantity=quantity,
                price=variant.price,
                total_price=variant.price * quantity
            )

        return order

    def calculate_subtotal(self, products):
        subtotal = 0
        for product in products:
            variant = ProductVariant.objects.get(id=product['variant_id'])
            subtotal += variant.price * product['quantity']
        return subtotal


class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SliderImage
        fields = ['id', 'image_url', 'alt_text', 'url', 'title', 'subtitle', 'order']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


## Flash Deal

class FlashDealSerializer(serializers.ModelSerializer):
    product_variants = serializers.SerializerMethodField()

    class Meta:
        model = FlashDeal
        fields = [
            'id', 'title', 'description', 'banner_image', 'start_date', 'end_date',
            'is_active', 'created_at', 'product_variants'
        ]

    def get_product_variants(self, obj):
        """
        Extract IDs from `product_variants`, fetch corresponding ProductVariant objects,
        and serialize them.
        """
        # Extract IDs from product_variants field
        variant_ids = [entry.get('id') for entry in obj.product_variants if 'id' in entry]
        # Query the ProductVariant model
        variants = ProductVariant.objects.filter(id__in=variant_ids, is_active=True)
        # Serialize the ProductVariant objects
        return ProductVariantSerializer(variants, many=True).data


class SupportTicketMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = SupportTicketMessage
        fields = ['id', 'ticket', 'sender', 'sender_name', 'message', 'created_at']
        read_only_fields = ['id', 'ticket', 'sender_name', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.username", read_only=True)
    messages = SupportTicketMessageSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            'ticket_id', 'name', 'user', 'user_name', 'assigned_to', 'assigned_to_name',
            'order', 'category', 'subject', 'description', 'solution', 'attachment',
            'status', 'priority', 'is_closed', 'created_at', 'updated_at', 'messages'
        ]
        read_only_fields = ['ticket_id', 'user_name', 'assigned_to_name', 'is_closed', 'created_at', 'updated_at',
                            'messages']
