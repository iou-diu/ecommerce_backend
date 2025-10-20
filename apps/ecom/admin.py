from django.contrib import admin
from .models import (
    Address, BusinessSetting, Category, Brand, Attribute, AttributeValue, Coupon, CustomerProfile, FlashDeal, Order,
    OrderLine, Payment, ShippingMethod, SliderImage, SupportTicket, SupportTicketMessage, Tag,
    Product, ProductImage, ProductAttribute, ProductVariant, StockEntry, Cart, CartItem, Transaction
)

admin.site.register(ProductAttribute)


# Inline for displaying Product Images within Product Admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# Inline for displaying Product Attributes within Product Admin
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


# Inline for displaying Cart Items within Cart Admin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


# Admin for Address model with search and filter options
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'full_name', 'address_line_1', 'city', 'country', 'is_default_shipping', 'is_default_billing')
    search_fields = ('full_name', 'address_line_1', 'city', 'country')
    list_filter = ('country', 'is_default_shipping', 'is_default_billing')
    autocomplete_fields = ['user']


# Admin for Category model with search and filter options
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    autocomplete_fields = ['parent']
    prepopulated_fields = {"slug": ("name",)}


# Admin for Brand model with search and filter options
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    prepopulated_fields = {"slug": ("name",)}


# Admin for Attribute model with search and filter options
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_type', 'is_filterable', 'is_variation')
    search_fields = ('name',)
    list_filter = ('data_type', 'is_filterable', 'is_variation')


# Admin for AttributeValue model with search and filter options
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    search_fields = ('value',)
    autocomplete_fields = ['attribute']


# Admin for Tag model with search options
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Admin for Product model with inlines for images and attributes, search, and filter options
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'meta_title')
    list_filter = ('category', 'brand', 'is_active', 'created_at')
    autocomplete_fields = ['category', 'brand', 'tags']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductAttributeInline]


# Admin for ProductVariant model with autocomplete and filter options
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'sku', 'price', 'is_active', 'stock_quantity')
    search_fields = ('sku', 'upc', 'product__name')
    list_filter = ('is_active',)
    autocomplete_fields = ['product', 'attributes']


# Admin for StockEntry model with search and filter options
@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ('variant', 'quantity', 'change_type', 'timestamp')
    search_fields = ('variant__sku',)
    list_filter = ('change_type', 'timestamp')
    autocomplete_fields = ['variant']


# Admin for Cart model with inlines for cart items, search, and filter options
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at', 'checked_out')
    search_fields = ('session_key', 'user__username')
    list_filter = ('checked_out', 'created_at')
    autocomplete_fields = ['user']
    inlines = [CartItemInline]


# Admin for CartItem model with autocomplete options
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'variant', 'quantity', 'added_at')
    search_fields = ('cart__user__username', 'variant__sku')
    autocomplete_fields = ['cart', 'variant']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_uuid', 'created_at', 'user', 'total_amount', 'status', 'payment_status')
    search_fields = ('user__email', 'order_uuid')
    list_filter = ('status', 'payment_status')


admin.site.register(OrderLine)
# admin.site.register(ShippingMethod)
admin.site.register(SupportTicket)
admin.site.register(SupportTicketMessage)
admin.site.register(CustomerProfile)

# admin.site.register(ShippingMethod)

admin.site.register(Coupon)


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'alt_text', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'alt_text')
    ordering = ('order',)


# class ProductVariantAdmin2(admin.ModelAdmin):
#     list_display = ('id', 'product', 'sku', 'price', 'stock_quantity')  # Add fields you want to display

# admin.site.register(ProductVariantAdmin2)

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost', 'is_active')  # Add other fields as necessary
    search_fields = ('name',)
    list_filter = ('is_active',)


admin.site.register(Transaction)
admin.site.register(Payment)

admin.site.register(BusinessSetting)
admin.site.register(FlashDeal)
