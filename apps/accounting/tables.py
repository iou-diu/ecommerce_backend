
import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe
from apps.helpers import CustomTable

from .models import Account, AccountHead, Bill, Expense, Payment, Transaction, TransactionLine

class AccountHeadTable(CustomTable):
    edit_url = 'accounthead_update'
    delete_url = 'accounthead_delete'
    class Meta:
        model = AccountHead
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'head_type']
        empty_text = 'No accountheads available'
        orderable = True
        exclude = ('selected',)

        
class AccountTable(CustomTable):
    edit_url = 'account_update'
    delete_url = 'account_delete'
    class Meta:
        model = Account
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'account_type', 'account_head', 'opening_balance', 'closing_balance', 'current_balance', 'is_closed']
        empty_text = 'No accounts available'
        orderable = True
        exclude = ('selected',)


class TransactionTable(CustomTable):
    edit_url = 'transaction_update'
    delete_url = 'transaction_delete'
    class Meta:
        model = Transaction
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['date', 'description', 'head']
        empty_text = 'No transactions available'
        orderable = True
        exclude = ('selected',)


class TransactionLineTable(CustomTable):
    edit_url = 'transactionline_update'
    delete_url = 'transactionline_delete'
    class Meta:
        model = TransactionLine
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['transaction', 'account', 'transaction_type', 'amount', 'date']
        empty_text = 'No transactionlines available'
        orderable = True
        exclude = ('selected',)


class BillTable(CustomTable):
    edit_url = 'bill_update'
    delete_url = 'bill_delete'
    class Meta:
        model = Bill
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['user', 'billing_date', 'due_date', 'total_amount', 'total_paid', 'total_due', 'status', 'transaction']
        empty_text = 'No bills available'
        orderable = True
        exclude = ('selected',)


class PaymentTable(CustomTable):
    edit_url = 'payment_update'
    delete_url = 'payment_delete'
    class Meta:
        model = Payment
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['user', 'bill', 'amount', 'payment_date']
        empty_text = 'No payments available'
        orderable = True
        exclude = ('selected',)
from .models import BusinessLocation

class BusinessLocationTable(CustomTable):
    edit_url = 'businesslocation_update'
    delete_url = 'businesslocation_delete'
    class Meta:
        model = BusinessLocation
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name']
        empty_text = 'No businesslocations available'
        orderable = True
        exclude = ('selected',)
from .models import ExpenseCategory

class ExpenseCategoryTable(CustomTable):
    edit_url = 'expensecategory_update'
    delete_url = 'expensecategory_delete'
    class Meta:
        model = ExpenseCategory
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'parent_category']
        empty_text = 'No expensecategorys available'
        orderable = True
        exclude = ('selected',)
from .models import PaymentAccount

class PaymentAccountTable(CustomTable):
    edit_url = 'paymentaccount_update'
    delete_url = 'paymentaccount_delete'
    class Meta:
        model = PaymentAccount
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'opening_balance', 'current_balance', 'account_type', 'is_active']
        empty_text = 'No paymentaccounts available'
        orderable = True
        exclude = ('selected',)
from .models import FundTransfer

class FundTransferTable(CustomTable):
    edit_url = 'fundtransfer_update'
    delete_url = 'fundtransfer_delete'
    class Meta:
        model = FundTransfer
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['from_account', 'to_account', 'amount', 'transfer_date', 'note']
        empty_text = 'No fundtransfers available'
        orderable = True
        exclude = ('selected',)


class ExpenseTable(CustomTable):
    action = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')
    class Meta:
        model = Expense
        template_name = 'django_tables2/bootstrap4.html'
        fields = [
            'business_location', 'category', 'reference_no', 'date', 
            'expense_for', 'contact', 'applicable_tax', 'total_amount',
            'remaining_balance', 'status',
        ]
        empty_text = 'No expenses available'
        orderable = True

    def render_action(self, record):
        """
        Render custom action buttons for the Expense table.
        """
        url = []
        details_url = reverse('expense_details_modal', args=[record.pk])
        details_button = f'<button type="button" class="btn btn-sm btn-light-info my-1" onclick="loadExpenseDetails(\'{details_url}\')"><i class="flaticon-eye"></i> View Details</button>'

        if self.view_perms and self.detail_url:
            detail_url = reverse(self.detail_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-info my-1"><i class="flaticon-eye"></i></a>' % detail_url)
        if self.edit_perms and self.edit_url:
            edit_url = reverse(self.edit_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-warning my-1"><i class="flaticon-edit"></i> Edit</a>' % edit_url)
        if self.delete_perms and self.delete_url:
            del_url = reverse(self.delete_url, args=[record.pk])
            url.append('<a href="%s" class="btn btn-sm btn-light-danger my-1"><i class="flaticon-delete"></i> Delete</a>' % del_url)

   
        add_payment_url = reverse('expensepayment_add_by_id', args=[record.pk])
        add_payment_button = f'<a href="{add_payment_url}" class="btn btn-sm btn-light-success py-1"><i class="flaticon-add"></i> Add Payment</a>'


        return mark_safe(f" {details_button} {add_payment_button} {' '.join(url)}")

from .models import ExpensePayment

class ExpensePaymentTable(CustomTable):
    edit_url = 'expensepayment_update'
    delete_url = 'expensepayment_delete'
    class Meta:
        model = ExpensePayment
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['expense', 'payment_account', 'amount', 'payment_date', 'note']
        empty_text = 'No expensepayments available'
        orderable = True
        exclude = ('selected',)
from .models import PaymentAccountDeposit

class PaymentAccountDepositTable(CustomTable):
    edit_url = 'paymentaccountdeposit_update'
    delete_url = 'paymentaccountdeposit_delete'
    class Meta:
        model = PaymentAccountDeposit
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['payment_account', 'amount', 'deposit_date', 'notes', 'document', 'created_at', 'updated_at']
        empty_text = 'No paymentaccountdeposits available'
        orderable = True
        exclude = ('selected',)