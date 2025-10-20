
import django_filters

from .models import Account, AccountHead, Bill, Expense, Payment, Transaction, TransactionLine

from .forms import AccountFilterForm, AccountHeadFilterForm, BillFilterForm, PaymentFilterForm, TransactionFilterForm, TransactionLineFilterForm

class AccountHeadFilter(django_filters.FilterSet):
    class Meta:
        model = AccountHead
        fields = ['name', 'head_type']
        form = AccountHeadFilterForm



class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'account_head', 'opening_balance', 'closing_balance', 'current_balance', 'is_closed']
        form = AccountFilterForm



class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'head']
        form = TransactionFilterForm



class TransactionLineFilter(django_filters.FilterSet):
    class Meta:
        model = TransactionLine
        fields = ['transaction', 'account', 'transaction_type', 'amount', 'date']
        form = TransactionLineFilterForm



class BillFilter(django_filters.FilterSet):
    class Meta:
        model = Bill
        fields = ['user', 'billing_date', 'due_date', 'total_amount', 'total_paid', 'total_due', 'status', 'transaction']
        form = BillFilterForm


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = ['user', 'bill', 'amount', 'payment_date']
        form = PaymentFilterForm

from .models import BusinessLocation

from .forms import BusinessLocationFilterForm

class BusinessLocationFilter(django_filters.FilterSet):
    class Meta:
        model = BusinessLocation
        fields = ['name']
        form = BusinessLocationFilterForm

from .models import ExpenseCategory

from .forms import ExpenseCategoryFilterForm

class ExpenseCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'parent_category']
        form = ExpenseCategoryFilterForm

from .models import PaymentAccount

from .forms import PaymentAccountFilterForm

class PaymentAccountFilter(django_filters.FilterSet):
    class Meta:
        model = PaymentAccount
        fields = ['name', 'opening_balance', 'current_balance', 'account_type', 'is_active']
        form = PaymentAccountFilterForm

from .models import FundTransfer

from .forms import FundTransferFilterForm

class FundTransferFilter(django_filters.FilterSet):
    class Meta:
        model = FundTransfer
        fields = ['from_account', 'to_account', 'amount', 'transfer_date', 'note']
        form = FundTransferFilterForm

from .forms import ExpenseFilterForm

class ExpenseFilter(django_filters.FilterSet):
    class Meta:
        model = Expense
        fields = ['business_location', 'category', 'reference_no', 'date', 'expense_for', 'contact', 'applicable_tax', 'total_amount',  'is_recurring', ]
        form = ExpenseFilterForm

from .models import ExpensePayment

from .forms import ExpensePaymentFilterForm

class ExpensePaymentFilter(django_filters.FilterSet):
    class Meta:
        model = ExpensePayment
        fields = ['expense', 'payment_account', 'amount', 'payment_date', 'note']
        form = ExpensePaymentFilterForm

from .models import PaymentAccountDeposit

from .forms import PaymentAccountDepositFilterForm

class PaymentAccountDepositFilter(django_filters.FilterSet):
    class Meta:
        model = PaymentAccountDeposit
        fields = ['payment_account', 'amount', 'deposit_date', 'notes', 'created_at', 'updated_at']
        form = PaymentAccountDepositFilterForm
