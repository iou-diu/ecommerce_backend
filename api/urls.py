from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.business_setting.views import BusinessSettingViewSet
from api.cms.views import HomeSliderViewSet, GalleryViewSet, BrochureViewSet, NewsPressViewSet, PublicSolutionViewSet, ContactFormViewSet
from api.ecom.cat_menu import MenuCategoryView
from api.ecom.hotspot import HotspotViewSet
from api.ecom.new_cart_api import MyCartViewSet
from api.ecom.views import AddressViewSet, CreateOrderView, FeaturedProductViewSet, FlashDealViewSet, \
    TransactionViewSet, PaymentVerifyView
from api.ecom.views import CategoryViewSet
from api.ecom.views import BrandViewSet
from api.ecom.views import AttributeViewSet
from api.ecom.views import AttributeValueViewSet
from api.ecom.views import TagViewSet
from api.ecom.views import ProductViewSet
from api.ecom.views import CartViewSet
from api.ecom.views import OrderViewSet
from api.ecom.views import CouponViewSet
from api.ecom.views import ShippingMethodViewSet
from api.ecom.views import WishlistViewSet
from api.ecom.views import WishlistItemViewSet
from api.ecom.views import ReviewViewSet
from api.ecom.views import ReviewReplyViewSet
from api.ecom.views import ReviewImageViewSet
from api.ecom.views import ProductFAQViewSet
from api.ecom.views import TaxViewSet
from api.ecom.views import PaymentViewSet, CheckoutViewSet
from api.ecom.views import AvailableProductsViewSet
from api.ecom.views import payment_success, CustomerProfileViewSet
from api.ecom.views import SliderImageAPIView
from api.ecom.views import OrderAndPaymentView
from api.ecom.views import NewArrivalAPIView
from api.products.views import FavoriteProductVariantViewSet
from api.ecom.PCBuilder import PCBuilderAPIView
from api.ecom.api_views import SupportTicketViewSet
from api.inventory.views import POCreateAPIView, PODetailAPIView, POViewSet, ProductVariantViewSet, \
    PublicProductVariantViewSet, PurchaseOrderCreateAPIView, PurchaseOrderDetailAPIView, PurchaseOrderUpdateAPIView, \
    RequisitionViewSet, SupplierViewSet, TestPayloadView
from api.products.views import ProductVariantCombinationAPIView, SimilarProductView, product_search_typesense
from api.user.auth import (
    OtpVerificationView,
    UserSignInView, PasswordResetView, PasswordResetConfirmView,
    UserSignUpView, UpdateUserInfoAPIView, PasswordChangeView,
)
from api.ecom.views import (
    ProductSearchViewSet,
    ProductDetailViewSet,
)

router = DefaultRouter()
router.register(r'variants', ProductVariantViewSet)
router.register(r'public-product-variants', PublicProductVariantViewSet, basename='public-product-variant')
router.register(r'requisitions', RequisitionViewSet)

router.register(r'address', AddressViewSet, basename='address')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'all_collections', BusinessSettingViewSet, basename='all_collections')

router.register(r'brand', BrandViewSet, basename='brand')
router.register(r'attribute', AttributeViewSet, basename='attribute')
router.register(r'attributevalue', AttributeValueViewSet, basename='attributevalue')
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'featured-products', FeaturedProductViewSet, basename='featured-products')

router.register(r'cart', CartViewSet, basename='cart')
router.register(r'my_cart', MyCartViewSet, basename='my_cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'transactionorder', TransactionViewSet, basename='transactionorder')
router.register(r'checkout', CheckoutViewSet, basename='checkout')
router.register(r'shipping', ShippingMethodViewSet, basename='shipping')

router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'coupon', CouponViewSet, basename='coupon')
# router.register(r'shippingmethod', ShippingMethodViewSet, basename='shippingmethod')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'wishlistitem', WishlistItemViewSet, basename='wishlistitem')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'review_reply', ReviewReplyViewSet, basename='review_reply')
router.register(r'reviewimage', ReviewImageViewSet, basename='reviewimage')
router.register(r'productfaq', ProductFAQViewSet, basename='productfaq')
router.register(r'tax', TaxViewSet, basename='tax')
router.register(r'available-products', AvailableProductsViewSet, basename='available-products')
router.register(r'product-search', ProductSearchViewSet, basename='product-search')
router.register(r'product-detail', ProductDetailViewSet, basename='product-detail')
router.register(r'favorite-variants', FavoriteProductVariantViewSet, basename='favorite-variants')

router.register(r'flash-deals', FlashDealViewSet, basename='flashdeal')
router.register(r'support-ticket', SupportTicketViewSet, basename='support-ticket')
# inventory router 

# router.register(r'order-payment/', OrderAndPaymentView, basename='order-payment/')

router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'po', POViewSet, basename='purchase-orders')
# router.register(r'sliders', SliderImageAPIView, basename='slider-list')

router.register(r'hotspots', HotspotViewSet, basename='hotspots')

# cms api router
router.register(r'home-slider', HomeSliderViewSet, basename='home-slider')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'brochures', BrochureViewSet, basename='brochures')
router.register(r'news-press', NewsPressViewSet, basename='news-press')
router.register(r'solutions', PublicSolutionViewSet, basename='solutions')
router.register(r'contact-form', ContactFormViewSet, basename='contact-form')

api_related_urlpatterns = [
    path('menu-categories/', MenuCategoryView.as_view(), name='menu_categories'),

    # user auth related urls
    path("signup/", UserSignUpView.as_view(), name="sign_up"),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path("otp-verify/", OtpVerificationView.as_view(), name="otp_verify"),
    path("signin/", UserSignInView.as_view(), name="sign_in"),
    path('profile/', UpdateUserInfoAPIView.as_view(), name='user_info'),

    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_conf'),

    path('order-payment/', OrderAndPaymentView.as_view(), name='order-payment'),
    path('product/<slug:product_slug>/variants/', ProductVariantCombinationAPIView.as_view(),
         name='product_variant_combinations'),
    path('test-payload/', TestPayloadView.as_view(), name='test-payload'),
    path('new_arrival/', NewArrivalAPIView.as_view(), name='new_arrival'),
    path('po/create/', POCreateAPIView.as_view(), name='po-create'),
    path('po/<int:pk>/', PODetailAPIView.as_view(), name='po-detail'),

    path('purchase-order/create/', PurchaseOrderCreateAPIView.as_view(), name='purchase-order-create'),
    path('purchase-order/<int:pk>/update/', PurchaseOrderUpdateAPIView.as_view(), name='purchase_order_update'),

    path('purchase-orders/<int:pk>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
    path('payment-success/', payment_success, name='payment-success'),

    path('product_search/', product_search_typesense, name='product_search'),
    path('similar_product_search/', SimilarProductView.as_view(), name='similar_product_search'),

    # custom cart
    path('orders/create/', OrderAndPaymentView.as_view(), name='order-create'),
    path('payment-verify/', PaymentVerifyView.as_view(), name='payment-verify'),

    path('update-profile/', CustomerProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
         name='profile-update'),
    path('sliders/', SliderImageAPIView.as_view(), name='slider-list'),

    path("pc-builder/", PCBuilderAPIView.as_view(), name="pc-builder"),

    # path('requisition/<int:requisition_id>/details/', get_requisition_details, name='requisition-details'),

    path('', include(router.urls)),

]
