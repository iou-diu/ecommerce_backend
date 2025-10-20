# serializers.py
from rest_framework import serializers
from api.ecom.serializers import TaxSerializer
from apps.ecom.models import ProductVariant, Tax
from apps.inventory.models import PO, AdditionalCost, POAdditionalCost, POItem, PurchaseOrder, PurchaseOrderItem, Requisition, RequisitionItem, Supplier
from decimal import Decimal


class PublicProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'upc', 'retail_price', 'is_active', 'attributes', 'image', 'stock_quantity']

        
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku', 'upc', 'price', 'retail_price', 'is_active', 'attributes', 'image', 'stock_quantity']
        depth = 1  # To include the related `product` and `attributes`


class ProductVariantRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku', 'upc', 'price', 'retail_price','stock_quantity']
        depth = 1  # To include the related `product` and `attributes`


class RequisitionItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantRequisitionSerializer()

    class Meta:
        model = RequisitionItem
        fields = ['variant', 'quantity']


class RequisitionSerializer(serializers.ModelSerializer):
    # Include items from the reverse relationship
    items = RequisitionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Requisition
        fields = ['id', 'requested_by', 'created_at', 'approved', 'approved_by', 'notes', 'items']




class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'



class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer()
    tax_model = TaxSerializer()
    selling_tax_model = TaxSerializer()
    quantity_ordered = serializers.IntegerField()
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrderItem
        fields = ['variant', 'quantity_ordered', 'price_per_unit', 'discount', 'tax','tax_model','profit_margin_percentage','expected_selling_price','selling_tax_model']

    def get_discount(self, obj):
        # Return as an integer if possible, or as-is if it has decimal places
        return int(obj.discount) if obj.discount == obj.discount.to_integral_value() else obj.discount

    def get_tax(self, obj):
        # Return as an integer if possible, or None if no tax is provided
        return int(obj.tax) if obj.tax and obj.tax == obj.tax.to_integral_value() else obj.tax or None

class AdditionalCostSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='description')
    value = serializers.SerializerMethodField()

    class Meta:
        model = AdditionalCost
        fields = ['key', 'value']

    def get_value(self, obj):
        # Return as an integer if possible, or as-is if it has decimal places
        return int(obj.amount) if obj.amount == obj.amount.to_integral_value() else obj.amount

class PurchaseOrderSerializer(serializers.ModelSerializer):
    requisition = serializers.IntegerField(source='requisition.id')
  
    order_date = serializers.SerializerMethodField()  # Use custom method
    global_discount_type = serializers.CharField()
    global_discount_value = serializers.SerializerMethodField()
    shipping_cost = serializers.SerializerMethodField()
    purchase_tax_value = serializers.SerializerMethodField()
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    additional_costs = AdditionalCostSerializer(many=True, read_only=True)
    purchase_tax_id = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            'requisition', 'supplier', 'order_date', 'status',
            'global_discount_type', 'global_discount_value',
            'shipping_info', 'shipping_cost',
            'purchase_tax_name', 'purchase_tax_id', 'purchase_tax_type',
            'purchase_tax_value', 'items', 'additional_costs','expected_delivery_date','paymentDays','paymentMonths'
        ]

    def get_order_date(self, obj):
        # Convert DateTimeField to Date format (YYYY-MM-DD)
        return obj.order_date.date().isoformat()  # Returns date without timezone

    def get_global_discount_value(self, obj):
        return int(obj.global_discount_value) if obj.global_discount_value == obj.global_discount_value.to_integral_value() else obj.global_discount_value

    def get_shipping_cost(self, obj):
        return int(obj.shipping_cost) if obj.shipping_cost == obj.shipping_cost.to_integral_value() else obj.shipping_cost

    def get_purchase_tax_value(self, obj):
        return int(obj.purchase_tax_value) if obj.purchase_tax_value == obj.purchase_tax_value.to_integral_value() else obj.purchase_tax_value

    def get_purchase_tax_id(self, obj):
        tax = Tax.objects.filter(name=obj.purchase_tax_name).first()
        return tax.id if tax else None
    








# PO Serializers
class POAdditionalCostSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='description')
    value = serializers.SerializerMethodField()

    class Meta:
        model = POAdditionalCost
        fields = ['key', 'value']

    def get_value(self, obj):
        # Return as an integer if possible, or as-is if it has decimal places
        return int(obj.amount) if obj.amount == obj.amount.to_integral_value() else obj.amount
    
    
class POItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer()
    tax_model = TaxSerializer()
    quantity_ordered = serializers.IntegerField()
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()

    class Meta:
        model = POItem
        fields = ['variant', 'quantity_ordered', 'price_per_unit', 'discount', 'tax','tax_model']

    def get_discount(self, obj):
        # Return as an integer if possible, or as-is if it has decimal places
        return int(obj.discount) if obj.discount == obj.discount.to_integral_value() else obj.discount

    def get_tax(self, obj):
        # Return as an integer if possible, or None if no tax is provided
        return int(obj.tax) if obj.tax and obj.tax == obj.tax.to_integral_value() else obj.tax or None
    


class POSerializer(serializers.ModelSerializer):
    requisition = serializers.IntegerField(source='requisition.id')
  
    order_date = serializers.SerializerMethodField()  # Use custom method
    global_discount_type = serializers.CharField()
    global_discount_value = serializers.SerializerMethodField()
    shipping_cost = serializers.SerializerMethodField()
    purchase_tax_value = serializers.SerializerMethodField()
    po_items = POItemSerializer(many=True, read_only=True)
    po_additional_costs = POAdditionalCostSerializer(many=True, read_only=True)
    purchase_tax_id = serializers.SerializerMethodField()

    class Meta:
        model = PO
        fields = ['id',
            'requisition', 'supplier', 'order_date', 'status',
            'global_discount_type', 'global_discount_value',
            'shipping_info', 'shipping_cost',
            'purchase_tax_name', 'purchase_tax_id', 'purchase_tax_type',
            'purchase_tax_value', 'po_items', 'po_additional_costs','expected_delivery_date','paymentDays','paymentMonths'
        ]

    def get_order_date(self, obj):
        # Convert DateTimeField to Date format (YYYY-MM-DD)
        return obj.order_date.date().isoformat()  # Returns date without timezone

    def get_global_discount_value(self, obj):
        return int(obj.global_discount_value) if obj.global_discount_value == obj.global_discount_value.to_integral_value() else obj.global_discount_value

    def get_shipping_cost(self, obj):
        return int(obj.shipping_cost) if obj.shipping_cost == obj.shipping_cost.to_integral_value() else obj.shipping_cost

    def get_purchase_tax_value(self, obj):
        return int(obj.purchase_tax_value) if obj.purchase_tax_value == obj.purchase_tax_value.to_integral_value() else obj.purchase_tax_value

    def get_purchase_tax_id(self, obj):
        tax = Tax.objects.filter(name=obj.purchase_tax_name).first()
        return tax.id if tax else None