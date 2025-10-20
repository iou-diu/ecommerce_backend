from django.urls import path

from .bulk_variant import ProductVariantBulkView
from .views import AttributeCreateView, AttributeDeleteView, AttributeListView, AttributeUpdateView, CouponListView, \
    FlashDealCreateEditView, FlashDealDeleteView, FlashDealView, ProductAttributeCreateViewDynamic, \
    ProductImageDirectCreateView, StockUpdateByProductViewDynamic, VariantSearchView, delete_product_attribute_values, \
    delete_product_image, save_menu_categories
from .views import AttributeValueCreateView, AttributeValueDeleteView, AttributeValueListView, AttributeValueUpdateView
from .views import TagCreateView, TagDeleteView, TagListView, TagUpdateView
from .views import TaxCreateView, TaxDeleteView, TaxListView, TaxUpdateView
from .views import ProductCreateView, ProductDeleteView, ProductListView, ProductUpdateView
from .views import ProductImageCreateView, ProductImageDeleteView, ProductImageListView, ProductImageUpdateView
from .views import ProductVariantCreateView, ProductVariantDeleteView, ProductVariantListView, ProductVariantUpdateView
from .views import StockEntryCreateView, StockEntryDeleteView, StockEntryListView, StockEntryUpdateView
from .views import OrderCreateView, OrderDeleteView, OrderListView, OrderUpdateView

from apps.ecom.products_view import ProductCreateView2, get_attribute_values
from .views import CategoryCreateView, CategoryDeleteView, CategoryListView, CategoryUpdateView, typesense_demo
from .views import AddressCreateView, AddressDeleteView, AddressListView, AddressUpdateView
from .views import BrandCreateView, BrandDeleteView, BrandListView, BrandUpdateView
from .views import generate_barcode
from django.views.generic import TemplateView
from . import ticket_views
from .views import CreateCouponView
from . import views
from .generate_meta import generate_meta, generate_meta_category
from .views import get_dashboard_data

urlpatterns = [
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/add/', OrderCreateView.as_view(), name='order_add'),
    path('order/', OrderListView.as_view(), name='order_list'),

    # --- new endpoints for modal data and status updates ---
    path('order/<int:pk>/detail-json/', views.order_detail_json, name='order_detail_json'),
    path('order/<int:pk>/update-status/', views.order_update_status, name='order_update_status'),
    # --- end new endpoints ---

    path('stockentry/<int:pk>/delete/', StockEntryDeleteView.as_view(), name='stockentry_delete'),
    path('stockentry/<int:pk>/update/', StockEntryUpdateView.as_view(), name='stockentry_update'),
    path('stockentry/update_stock/<int:variant_id>/', StockUpdateByProductViewDynamic.as_view(),
         name='stock_product_wise_update'),
    path('stockentry/add/', StockEntryCreateView.as_view(), name='stockentry_add'),
    path('stockentry/', StockEntryListView.as_view(), name='stockentry_list'),

    path('productvariant/<int:pk>/delete/', ProductVariantDeleteView.as_view(), name='productvariant_delete'),
    path('productvariant/<int:pk>/update/', ProductVariantUpdateView.as_view(), name='productvariant_update'),

    path('productvariant/<int:pk>/bulk_add/', ProductVariantBulkView.as_view(), name='productvariant_bulk'),

    path('productvariant/add/', ProductVariantCreateView.as_view(), name='productvariant_add'),
    path('productvariant/', ProductVariantListView.as_view(), name='productvariant_list'),
    path('product/images/<int:product_id>/', ProductImageDirectCreateView.as_view(), name='product_add_images'),
    path('delete-image/<int:image_id>/', delete_product_image, name='delete_product_image'),
    path('productimage/<int:pk>/delete/', ProductImageDeleteView.as_view(), name='productimage_delete'),
    path('productimage/<int:pk>/update/', ProductImageUpdateView.as_view(), name='productimage_update'),
    path('productimage/add/', ProductImageCreateView.as_view(), name='productimage_add'),
    path('productimage/', ProductImageListView.as_view(), name='productimage_list'),
    path('product/attributes/<int:product_id>/', ProductAttributeCreateViewDynamic.as_view(),
         name='product_attribute_dynamic_create'),
    path('product-attributes-dynamic/delete-values/<int:product_id>/', delete_product_attribute_values,
         name='delete_product_attribute_values'),

    path('stock-entry/<int:stock_entry_id>/generate/', generate_barcode, name='generate_barcode'),

    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('tax/<int:pk>/delete/', TaxDeleteView.as_view(), name='tax_delete'),
    path('tax/<int:pk>/update/', TaxUpdateView.as_view(), name='tax_update'),
    path('tax/add/', TaxCreateView.as_view(), name='tax_add'),
    path('tax/', TaxListView.as_view(), name='tax_list'),
    path('tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    path('tag/<int:pk>/update/', TagUpdateView.as_view(), name='tag_update'),
    path('tag/add/', TagCreateView.as_view(), name='tag_add'),
    path('tag/', TagListView.as_view(), name='tag_list'),
    path('attributevalue/<int:pk>/delete/', AttributeValueDeleteView.as_view(), name='attributevalue_delete'),
    path('attributevalue/<int:pk>/update/', AttributeValueUpdateView.as_view(), name='attributevalue_update'),
    path('attributevalue/add/', AttributeValueCreateView.as_view(), name='attributevalue_add'),
    path('attributevalue/', AttributeValueListView.as_view(), name='attributevalue_list'),
    path('attribute/<int:pk>/delete/', AttributeDeleteView.as_view(), name='attribute_delete'),
    path('attribute/<int:pk>/update/', AttributeUpdateView.as_view(), name='attribute_update'),
    path('attribute/add/', AttributeCreateView.as_view(), name='attribute_add'),
    path('attribute/', AttributeListView.as_view(), name='attribute_list'),
    path('brand/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand_delete'),
    path('brand/<int:pk>/update/', BrandUpdateView.as_view(), name='brand_update'),
    path('brand/add/', BrandCreateView.as_view(), name='brand_add'),
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
    path('address/<int:pk>/update/', AddressUpdateView.as_view(), name='address_update'),
    path('address/add/', AddressCreateView.as_view(), name='address_add'),
    path('address/', AddressListView.as_view(), name='address_list'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('add-product/', ProductCreateView2.as_view(), name='add_product'),
    path('get-attribute-values/', get_attribute_values, name='get_attribute_values'),
    path('typesense_demo/', typesense_demo, name='typesense_demo'),

    path('tickets/', ticket_views.SupportTicketListView.as_view(), name='support_ticket_list'),
    path('tickets/create/', ticket_views.SupportTicketCreateView.as_view(), name='support_ticket_create'),
    path('tickets/<str:ticket_id>/', ticket_views.SupportTicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<str:ticket_id>/assign/', ticket_views.SupportTicketAssignView.as_view(),
         name='support_ticket_assign'),
    path('tickets/<str:ticket_id>/close/', ticket_views.SupportTicketCloseView.as_view(), name='support_ticket_close'),
    path('create-coupon/', CreateCouponView.as_view(), name='create-coupon'),

    path('coupons/', CouponListView.as_view(), name='coupon-list'),
    path('slider-images/', views.SliderImageListView.as_view(), name='slider_image_list'),
    path('slider-images/create/', views.SliderImageCreateView.as_view(), name='slider_image_create'),
    path('slider-images/<int:pk>/edit/', views.SliderImageUpdateView.as_view(), name='slider_image_update'),
    path('slider-images/<int:pk>/delete/', views.SliderImageDeleteView.as_view(), name='slider_image_delete'),

    path('reindex/', views.reindex_view, name='reindex'),
    path('mega-menu/', views.ManageMenuView.as_view(), name='mega-menu'),
    path('save-menu-categories/', save_menu_categories, name='save_menu_categories'),
    path('save-banner-settings/', views.save_banner_settings, name='save_banner_settings'),

    path('flash-deals/', FlashDealView.as_view(), name='flash_deals'),
    path('flash-deals/create/', FlashDealCreateEditView.as_view(), name='flash_deal_create'),
    path('flash-deals/edit/<int:flash_deal_id>/', FlashDealCreateEditView.as_view(), name='flash_deal_edit'),
    path('variants/search/', VariantSearchView.as_view(), name='variant_search'),
    path('flash-deals/<int:pk>/delete/', FlashDealDeleteView.as_view(), name='flash_deals_delete'),
    path('generate-meta/', generate_meta, name='generate_meta'),
    path('generate-meta_category/', generate_meta, name='generate_meta_category'),
    path('dashboard-data/', get_dashboard_data, name='dashboard-data'),
]
