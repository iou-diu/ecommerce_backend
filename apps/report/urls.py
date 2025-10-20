from django.urls import path
from . import views
from .profit_loss import ProfitLossReportView
from .purchase_sales import PurchaseSaleReportView

urlpatterns = [
    path('purchase-sale/', PurchaseSaleReportView.as_view(), name='purchase_sale_report'),
    path('profit-loss/', ProfitLossReportView.as_view(), name='profit-loss_report'),

]
