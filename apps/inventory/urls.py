# inventory/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('requisitions/', views.RequisitionListView.as_view(), name='requisition_list'),
    path('requisition/create/', views.create_requisition, name='create_requisition'),
    path('requisitions/edit/<int:requisition_id>/', views.edit_requisition, name='edit_requisition'),
    path('requisitions/<int:requisition_id>/', views.requisition_detail, name='requisition_detail'),
    
    path('goods_received_note/create/<int:purchase_order_id>/', views.create_goods_received_note, name='create_goods_received_note'),
    # Add more URLs as needed
    path('add__test_stock/', views.add__test_stock, name='add__test_stock'),

    path('purchase-order/create/', views.purchase_order_form, name='purchase_order_create'),
    path('po/view/<int:pk>/', views.po_display, name='po_details_display'),

    # path('purchase_order/create/<int:requisition_id>/', views.create_purchase_order, name='create_purchase_order'),
    
    path('purchase-order/', views.POListView.as_view(), name='po_list'),
    path('list-purchases/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),

    path('add-purchase/', views.po_form, name='purchase_order_add'),

    path('purchase_order/edit/<int:pk>/', views.po_form_edit, name='purchase_order_edit'),
    path('purchase_order/view/<int:pk>/', views.purchase_display, name='purchase_order_display'),


    path('purchase_order_new/', views.po_new, name='purchase_order_new'),
    path('purchase_payment/add/<int:purchase_order_id>/',views.PurchasePaymentCreateByIDView.as_view(),name='purchase_payment_add_by_id'),

    path('purchase-order/<int:pk>/payments/', views.PurchaseOrderPaymentsModalView.as_view(), name='purchase_order_payments_modal'),


    
    
    path('supplier/', views.SupplierListView.as_view(), name='supplier_list'),
    path('supplier/add/', views.SupplierCreateView.as_view(), name='supplier_add'),
    path('supplier/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),

    path('approve/<int:pk>/', views.approve_requisition, name='approve_requisition'),
    path('pos/', views.pos_form, name='pos_form'),
]