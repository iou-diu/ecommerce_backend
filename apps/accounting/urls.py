from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessLocationCreateView, BusinessLocationDeleteView, BusinessLocationListView, BusinessLocationUpdateView, ExpenseDetailsModalView, ExpensePaymentCreateByIDView
from .views import ExpenseCategoryCreateView, ExpenseCategoryDeleteView, ExpenseCategoryListView, ExpenseCategoryUpdateView
from .views import PaymentAccountCreateView, PaymentAccountDeleteView, PaymentAccountListView, PaymentAccountUpdateView
from .views import FundTransferCreateView, FundTransferDeleteView, FundTransferListView, FundTransferUpdateView
from .views import ExpenseCreateView, ExpenseDeleteView, ExpenseListView, ExpenseUpdateView
from .views import ExpensePaymentCreateView, ExpensePaymentDeleteView, ExpensePaymentListView, ExpensePaymentUpdateView
from .views import PaymentAccountDepositCreateView, PaymentAccountDepositListView

from apps.user.access import superuser_or_admin_required
from . import views
from .views import (
    PaymentCreateView, PaymentDeleteView, PaymentListView, PaymentUpdateView,
    BillCreateView, BillDeleteView, BillListView, BillUpdateView,
    AccountHeadCreateView, AccountHeadDeleteView, AccountHeadListView, AccountHeadUpdateView,
    AccountCreateView, AccountDeleteView, AccountListView, AccountUpdateView, CompleteBillCreateView, CompletePaymentCreateView, TransactionAddLinesView,
    TransactionCreateView, TransactionCreateViewNew, TransactionDeleteView, TransactionListView, TransactionUpdateView,
    TransactionLineCreateView, TransactionLineDeleteView, TransactionLineListView, TransactionLineUpdateView, get_payments_for_bill
)

# Router for API views
router = DefaultRouter()
router.register(r'transactions-list', views.TransactionViewSet)
router.register(r'transaction-lines', views.TransactionLineViewSet)

# edit delete permission need to discuss 

urlpatterns = [
    # path('paymentaccountdeposit/<int:pk>/delete/', PaymentAccountDepositDeleteView.as_view(), name='paymentaccountdeposit_delete'),
    # path('paymentaccountdeposit/<int:pk>/update/', PaymentAccountDepositUpdateView.as_view(), name='paymentaccountdeposit_update'),
    path('paymentaccountdeposit/add/', PaymentAccountDepositCreateView.as_view(), name='paymentaccountdeposit_add'),
    path('paymentaccountdeposit/', PaymentAccountDepositListView.as_view(), name='paymentaccountdeposit_list'),
    path('expensepayment/add/<int:expense_id>/', ExpensePaymentCreateByIDView.as_view(), name='expensepayment_add_by_id'),
    path('expensepayment/<int:pk>/delete/', ExpensePaymentDeleteView.as_view(), name='expensepayment_delete'),
    path('expensepayment/<int:pk>/update/', ExpensePaymentUpdateView.as_view(), name='expensepayment_update'),
    path('expensepayment/add/', ExpensePaymentCreateView.as_view(), name='expensepayment_add'),
    path('expensepayment/', ExpensePaymentListView.as_view(), name='expensepayment_list'),
    path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    path('expense/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense/add/', ExpenseCreateView.as_view(), name='expense_add'),
    path('expense/<int:pk>/details/', ExpenseDetailsModalView.as_view(), name='expense_details_modal'),
    path('expense/', ExpenseListView.as_view(), name='expense_list'),
    path('fundtransfer/<int:pk>/delete/', FundTransferDeleteView.as_view(), name='fundtransfer_delete'),
    path('fundtransfer/<int:pk>/update/', FundTransferUpdateView.as_view(), name='fundtransfer_update'),
    path('fundtransfer/add/', FundTransferCreateView.as_view(), name='fundtransfer_add'),
    path('fundtransfer/', FundTransferListView.as_view(), name='fundtransfer_list'),
    path('paymentaccount/<int:pk>/delete/', PaymentAccountDeleteView.as_view(), name='paymentaccount_delete'),
    path('paymentaccount/<int:pk>/update/', PaymentAccountUpdateView.as_view(), name='paymentaccount_update'),
    path('paymentaccount/add/', PaymentAccountCreateView.as_view(), name='paymentaccount_add'),
    path('paymentaccount/', PaymentAccountListView.as_view(), name='paymentaccount_list'),
    path('expensecategory/<int:pk>/delete/', ExpenseCategoryDeleteView.as_view(), name='expensecategory_delete'),
    path('expensecategory/<int:pk>/update/', ExpenseCategoryUpdateView.as_view(), name='expensecategory_update'),
    path('expensecategory/add/', ExpenseCategoryCreateView.as_view(), name='expensecategory_add'),
    path('expensecategory/', ExpenseCategoryListView.as_view(), name='expensecategory_list'),
    path('businesslocation/<int:pk>/delete/', BusinessLocationDeleteView.as_view(), name='businesslocation_delete'),
    path('businesslocation/<int:pk>/update/', BusinessLocationUpdateView.as_view(), name='businesslocation_update'),
    path('businesslocation/add/', BusinessLocationCreateView.as_view(), name='businesslocation_add'),
    path('businesslocation/', BusinessLocationListView.as_view(), name='businesslocation_list'),
    
    
    



    # AccountHead URLs
    path('accounthead/', superuser_or_admin_required(AccountHeadListView.as_view()), name='accounthead_list'),
    path('accounthead/add/', superuser_or_admin_required(AccountHeadCreateView.as_view()), name='accounthead_add'),
    path('accounthead/<int:pk>/update/', superuser_or_admin_required(AccountHeadUpdateView.as_view()), name='accounthead_update'),
    path('accounthead/<int:pk>/delete/', superuser_or_admin_required(AccountHeadDeleteView.as_view()), name='accounthead_delete'),

    # Account URLs
    path('account/', superuser_or_admin_required(AccountListView.as_view()), name='account_list'),
    path('account/add/', superuser_or_admin_required(AccountCreateView.as_view()), name='account_add'),
    path('account/<int:pk>/update/', superuser_or_admin_required(AccountUpdateView.as_view()), name='account_update'),
    path('account/<int:pk>/delete/', superuser_or_admin_required(AccountDeleteView.as_view()), name='account_delete'),

    # Transaction URLs
    path('transaction/', superuser_or_admin_required(TransactionListView.as_view()), name='transaction_list'),
    path('transaction/add/', superuser_or_admin_required(TransactionCreateView.as_view()), name='transaction_add'),
    path('transaction/<int:pk>/update/', superuser_or_admin_required(TransactionUpdateView.as_view()), name='transaction_update'),
    path('transaction/<int:pk>/delete/', superuser_or_admin_required(TransactionDeleteView.as_view()), name='transaction_delete'),

    # TransactionLine URLs
    path('transactionline/', superuser_or_admin_required(TransactionLineListView.as_view()), name='transactionline_list'),
    path('transactionline/add/', superuser_or_admin_required(TransactionCreateViewNew.as_view()), name='transactionline_add'),
    path('transaction/<int:transaction_id>/add-lines/', superuser_or_admin_required(TransactionAddLinesView.as_view()), name='transaction_add_lines'),
    path('transactionline/<int:pk>/update/', superuser_or_admin_required(TransactionLineUpdateView.as_view()), name='transactionline_update'),
    path('transactionline/<int:pk>/delete/', superuser_or_admin_required(TransactionLineDeleteView.as_view()), name='transactionline_delete'),

    # API router
    # path('', include(router.urls)),

    # Custom transaction views
    path('create-transaction/', superuser_or_admin_required(views.create_transaction_view), name='create_transaction'),
    path('transactions-old/', superuser_or_admin_required(views.transaction_list), name='transaction_list_old'),
    path('transactions-old/<int:pk>/', superuser_or_admin_required(views.transaction_detail), name='transaction_detail'),


    path('payment/', superuser_or_admin_required(PaymentListView.as_view()), name='payment_list'),
    # path('payment/add/', PaymentCreateView.as_view(), name='payment_add'),
    # path('payment/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    # path('payment/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
    
    path('bill/', superuser_or_admin_required(BillListView.as_view()), name='bill_list'),
    # path('bill/add/', BillCreateView.as_view(), name='bill_add'),
    # path('bill/<int:pk>/update/', BillUpdateView.as_view(), name='bill_update'),
    # path('bill/<int:pk>/delete/', BillDeleteView.as_view(), name='bill_delete'),


    # bills and payments
    path('bills/create/', superuser_or_admin_required(CompleteBillCreateView.as_view()), name='bill_create'),

    # URL to take a payment for a bill
    path('payments/create/',superuser_or_admin_required( CompletePaymentCreateView.as_view()), name='payment_create'),
    path('payments-for-bill/', get_payments_for_bill, name='payments_for_bill'),



]
