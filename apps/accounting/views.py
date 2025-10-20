from django.shortcuts import render, redirect,get_object_or_404
from decimal import Decimal
from django.views.generic.detail import DetailView
from django.contrib import messages  
from django.views.generic import UpdateView
from django.forms import inlineformset_factory
from django.db import transaction
from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.http import JsonResponse



from apps.accounting.filters import AccountFilter, AccountHeadFilter, BillFilter, PaymentFilter, TransactionFilter, TransactionLineFilter
from apps.accounting.forms import AccountForm, AccountHeadForm, BaseTransactionLineFormSet, BillForm, CompleteBillForm, CompletePaymentForm, PaymentForm, TransactionForm, TransactionLineForm, TransactionLineFormSetNew
from apps.accounting.models import Account, AccountHead, Bill, Payment, Transaction, TransactionLine
from apps.accounting.tables import AccountHeadTable, AccountTable, BillTable, PaymentTable, TransactionLineTable, TransactionTable
from apps.helpers import CustomSingleTableMixin, MessageMixin, PageHeaderMixin

from .serializers import AccountHeadSerializer, AccountSerializer, TransactionSerializer, TransactionLineSerializer



def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transaction_detail.html', {'transaction': transaction})


def transaction_list(request):
    transactions = Transaction.objects.all()  # Fetch all transactions from the database
    return render(request, 'transaction_list.html', {'transactions': transactions})


def create_transaction_view(request):


    return render(request, 'create_transaction.html')


class AccountHeadListView(generics.ListAPIView):
    queryset = AccountHead.objects.all()
    serializer_class = AccountHeadSerializer

class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionLineViewSet(viewsets.ModelViewSet):
    queryset = TransactionLine.objects.all()
    serializer_class = TransactionLineSerializer



class AccountHeadListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = AccountHead
    table_class = AccountHeadTable
    template_name = 'list.html'
    filterset_class = AccountHeadFilter
    #ordering = ['some_field']
    page_title = 'All Account Heads'
    add_link = reverse_lazy('accounthead_add')
    add_perms = 'accounthead.add_accounthead'
    edit_perms = 'accounthead.change_accounthead'
    delete_perms = 'accounthead.delete_accounthead'

class AccountHeadCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = AccountHead
    form_class = AccountHeadForm
    template_name = 'add.html'
    success_url = reverse_lazy('accounthead_list')
    page_title = 'Account Head'
    list_link = reverse_lazy('accounthead_list')

class AccountHeadUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    model = AccountHead
    form_class = AccountHeadForm
    template_name = 'add.html'
    success_url = reverse_lazy('accounthead_list')
    page_title = 'Update Account Head'
    list_link = reverse_lazy('accounthead_list')

class AccountHeadDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = AccountHead
    template_name = 'delete.html'
    page_title = 'Delete Account Head'
    success_url = reverse_lazy('accounthead_list')



class AccountListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Account
    table_class = AccountTable
    template_name = 'list.html'
    filterset_class = AccountFilter
    #ordering = ['some_field']
    page_title = 'All Accounts'
    add_link = reverse_lazy('account_add')
    add_perms = 'account.add_account'
    edit_perms = 'account.change_account'
    delete_perms = 'account.delete_account'

class AccountCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'add.html'
    success_url = reverse_lazy('account_list')
    page_title = 'Account'
    list_link = reverse_lazy('account_list')

class AccountUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'add.html'
    success_url = reverse_lazy('account_list')
    page_title = 'Update Account'
    list_link = reverse_lazy('account_list')

class AccountDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = Account
    template_name = 'delete.html'
    page_title = 'Delete Account'
    success_url = reverse_lazy('account_list')



class TransactionListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Transaction
    table_class = TransactionTable
    template_name = 'list.html'
    filterset_class = TransactionFilter
    #ordering = ['some_field']
    page_title = 'All Transactions'
    add_link = reverse_lazy('transaction_add')
    add_perms = 'transaction.add_transaction'
    # edit_perms = 'transaction.change_transaction'
    # delete_perms = 'transaction.delete_transaction'

class TransactionCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'add.html'
    success_url = reverse_lazy('transaction_list')
    page_title = 'Transaction'
    list_link = reverse_lazy('transaction_list')

class TransactionUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'add.html'
    success_url = reverse_lazy('transaction_list')
    page_title = 'Update Transaction'
    list_link = reverse_lazy('transaction_list')

class TransactionDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = Transaction
    template_name = 'delete.html'
    page_title = 'Delete Transaction'
    success_url = reverse_lazy('transaction_list')



class TransactionLineListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = TransactionLine
    table_class = TransactionLineTable
    template_name = 'list.html'
    filterset_class = TransactionLineFilter
    #ordering = ['some_field']
    page_title = 'All Transaction Lines'
    add_link = reverse_lazy('transactionline_add')
    add_perms = 'transactionline.add_transactionline'
    # edit_perms = 'transactionline.change_transactionline'
    # delete_perms = 'transactionline.delete_transactionline'

class TransactionLineCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = TransactionLine
    form_class = TransactionLineForm
    template_name = 'add.html'
    success_url = reverse_lazy('transactionline_list')
    page_title = 'Transaction Line'
    list_link = reverse_lazy('transactionline_list')

class TransactionLineUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    model = TransactionLine
    form_class = TransactionLineForm
    template_name = 'add.html'
    success_url = reverse_lazy('transactionline_list')
    page_title = 'Update Transaction Line'
    list_link = reverse_lazy('transactionline_list')

class TransactionLineDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = TransactionLine
    template_name = 'delete.html'
    page_title = 'Delete Transaction Line'
    success_url = reverse_lazy('transactionline_list')


# double entry accounting system

class TransactionCreateViewNew(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form2.html'
    success_url = reverse_lazy('transactionline_list')
    page_title = 'Transaction and Lines'
    list_link = reverse_lazy('transactionline_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['lines'] = TransactionLineFormSetNew(self.request.POST)
        else:
            data['lines'] = TransactionLineFormSetNew()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lines = context['lines']
        if lines.is_valid():
            with transaction.atomic():
                self.object = form.save()
                lines.instance = self.object
                lines.save()
            return super().form_valid(form)
        else:
            # Return form_invalid with form errors
            return self.form_invalid(form)



class TransactionAddLinesView(UpdateView):
    model = Transaction
    fields = []
    template_name = 'transaction_add_lines.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        transaction = get_object_or_404(Transaction, id=self.kwargs['transaction_id'])

        existing_lines = transaction.lines.all()
        data['existing_lines'] = existing_lines
        if existing_lines.exists():
            total_debit = sum(line.amount for line in transaction.lines.filter(transaction_type='debit'))
            total_credit = sum(line.amount for line in transaction.lines.filter(transaction_type='credit'))
        else:
            total_debit = 0
            total_credit = 0

        data['total_debit'] = total_debit
        data['total_credit'] = total_credit

        # Initialize formset for new TransactionLine entries
        TransactionLineFormSet = inlineformset_factory(
            Transaction,
            TransactionLine,
            form=TransactionLineForm,
            formset=BaseTransactionLineFormSet,
            extra=2,
            can_delete=False
        )

        if self.request.POST:
            data['lines'] = TransactionLineFormSet(self.request.POST, instance=transaction)
        else:
            data['lines'] = TransactionLineFormSet(instance=transaction)

        for form in data['lines'].forms:
            if form.instance.pk:
                form.visible = False

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lines = context['lines']

        if lines.is_valid():
            with transaction.atomic():
                lines.instance = self.object
                lines.save()

            # Add a success message
            messages.success(self.request, 'Transaction lines saved successfully.')

            return redirect('transaction_add_lines', transaction_id=self.object.id)

        else:
            return self.form_invalid(form)

    def get_object(self):
        return get_object_or_404(Transaction, id=self.kwargs['transaction_id'])


# bill process sections
# transaction needs datetime 


class CompleteBillCreateView(CreateView):
    model = Bill
    form_class = CompleteBillForm
    template_name = 'bill_form.html'
    success_url = reverse_lazy('bill_create')

    def form_valid(self, form):
        with transaction.atomic():
            # Save the bill
            bill = form.save(commit=False)
            bill.save()

            # Get or create the Revenue AccountHead
            revenue_head, _ = AccountHead.objects.get_or_create(
                name="Revenue Account",
                defaults={'head_type': 'revenue'}
            )

            # Create a transaction for the bill
            bill_transaction = Transaction.objects.create(
                description=f"Bill for {bill.user}, due on {bill.due_date}",
                head=revenue_head,
            )

            # Get or create necessary AccountHeads and Accounts
            cash_head, _ = AccountHead.objects.get_or_create(
                name="Cash", defaults={'head_type': 'asset'}
            )
            cash_account, _ = Account.objects.get_or_create(
                name='Cash',
                defaults={'account_type': 'asset', 'account_head': cash_head}
            )

            receivable_head, _ = AccountHead.objects.get_or_create(
                name="Accounts Receivable", defaults={'head_type': 'asset'}
            )
            receivable_account, _ = Account.objects.get_or_create(
                name='Accounts Receivable',
                defaults={'account_type': 'asset', 'account_head': receivable_head}
            )

            payment_amount = Decimal('0')
            if form.cleaned_data.get('enable_payment') and form.cleaned_data.get('payment_amount'):
                payment_amount = Decimal(str(form.cleaned_data['payment_amount']))

            # Determine payment scenario
            if payment_amount == 0:  # No payment
                # Debit Accounts Receivable
                TransactionLine.objects.create(
                    transaction=bill_transaction,
                    account=receivable_account,
                    transaction_type='debit',
                    amount=bill.total_amount
                )
                bill.status = Bill.Status.UNPAID
            elif payment_amount == bill.total_amount:  # Full payment
                # Debit Cash
                TransactionLine.objects.create(
                    transaction=bill_transaction,
                    account=cash_account,
                    transaction_type='debit',
                    amount=bill.total_amount
                )
                bill.status = Bill.Status.PAID
            else:  # Partial payment
                # Debit Cash
                TransactionLine.objects.create(
                    transaction=bill_transaction,
                    account=cash_account,
                    transaction_type='debit',
                    amount=payment_amount
                )
                # Debit Accounts Receivable
                TransactionLine.objects.create(
                    transaction=bill_transaction,
                    account=receivable_account,
                    transaction_type='debit',
                    amount=bill.total_amount - payment_amount
                )
                bill.status = Bill.Status.PARTIALLY_PAID

            # Credit Revenue (always)
            credit_account = form.cleaned_data['credit_account']
            TransactionLine.objects.create(
                transaction=bill_transaction,
                account=credit_account,
                transaction_type='credit',
                amount=bill.total_amount
            )

            # Update bill's total_paid and total_due
            bill.total_paid = payment_amount
            bill.total_due = bill.total_amount - payment_amount
            bill.transaction = bill_transaction
            bill.save()

            if payment_amount > 0:
                Payment.objects.create(
                    user=bill.user,
                    bill=bill,
                    amount=payment_amount
                )

        messages.success(self.request, ' Bill has been created successfully.')
        return super().form_valid(form)
    

class CompletePaymentCreateView(CreateView):
    model = Payment
    form_class = CompletePaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        with transaction.atomic():
            payment = form.save(commit=False)
            bill = payment.bill

            # Ensure payment amount doesn't exceed the remaining due amount
            max_payment = bill.total_due
            if payment.amount > max_payment:
                form.add_error('amount', f'Payment cannot exceed the remaining due amount of {max_payment}')
                return self.form_invalid(form)

            # Create a corresponding transaction for the payment
            revenue_head, _ = AccountHead.objects.get_or_create(
                name="Revenue Account",
                defaults={'head_type': 'revenue'}
            )
            payment_transaction = Transaction.objects.create(
                description=f"Payment received for bill {bill.id}",
                 head=revenue_head,
            )

            # Debit Cash (Asset)
            cash_account = Account.objects.get(name='Cash')
            TransactionLine.objects.create(
                transaction=payment_transaction,
                account=cash_account,
                transaction_type='debit',
                amount=payment.amount
            )

            # Credit Accounts Receivable (Asset)
            receivable_account = Account.objects.get(name='Accounts Receivable')
            TransactionLine.objects.create(
                transaction=payment_transaction,
                account=receivable_account,
                transaction_type='credit',
                amount=payment.amount
            )

            # Apply payment to the bill and update the totals
            bill.total_paid += payment.amount
            bill.total_due -= payment.amount

            # Update bill status
            if bill.total_due == 0:
                bill.status = Bill.Status.PAID
            elif bill.total_due < bill.total_amount:
                bill.status = Bill.Status.PARTIALLY_PAID
            
            bill.save()
            payment.user = bill.user
            payment.save()

            messages.success(self.request, f'Payment of {payment.amount} has been successfully applied to the bill.')

        return super().form_valid(form)


class BillListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Bill
    table_class = BillTable
    template_name = 'list.html'
    filterset_class = BillFilter
    #ordering = ['some_field']
    page_title = 'All Bills'
    add_link = reverse_lazy('bill_create')
    add_perms = 'bill.add_bill'
    # edit_perms = 'bill.change_bill'
    # delete_perms = 'bill.delete_bill'

class BillCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'add.html'
    success_url = reverse_lazy('bill_list')
    page_title = 'Bill'
    list_link = reverse_lazy('bill_list')

class BillUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    model = Bill
    form_class = BillForm
    template_name = 'add.html'
    success_url = reverse_lazy('bill_list')
    page_title = 'Update Bill'
    list_link = reverse_lazy('bill_list')

class BillDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = Bill
    template_name = 'delete.html'
    page_title = 'Delete Bill'
    success_url = reverse_lazy('bill_list')



class PaymentListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Payment
    table_class = PaymentTable
    template_name = 'list.html'
    filterset_class = PaymentFilter
    #ordering = ['some_field']
    page_title = 'All Payments'
    add_link = reverse_lazy('payment_create')
    add_perms = 'payment.add_payment'
    # edit_perms = 'payment.change_payment'
    # delete_perms = 'payment.delete_payment'

class PaymentCreateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'add.html'
    success_url = reverse_lazy('payment_list')
    page_title = 'Payment'
    list_link = reverse_lazy('payment_list')

class PaymentUpdateView(LoginRequiredMixin, PageHeaderMixin, MessageMixin,UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'add.html'
    success_url = reverse_lazy('payment_list')
    page_title = 'Update Payment'
    list_link = reverse_lazy('payment_list')

class PaymentDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = Payment
    template_name = 'delete.html'
    page_title = 'Delete Payment'
    success_url = reverse_lazy('payment_list')


# show payments by bill 
def get_payments_for_bill(request):
    bill_id = request.GET.get('bill_id')
    if bill_id:
        payments = Payment.objects.filter(bill_id=bill_id).values('amount', 'payment_date', 'user')
        data = list(payments)
        return JsonResponse({'payments': data})
    return JsonResponse({'error': 'No bill ID provided'}, status=400)


from .models import BusinessLocation, Expense

from .forms import BusinessLocationForm, ExpensePaymentGeneralForm

from .tables import BusinessLocationTable

from .filters import BusinessLocationFilter




class BusinessLocationListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = BusinessLocation
    table_class = BusinessLocationTable
    template_name = 'list.html'
    filterset_class = BusinessLocationFilter
    #ordering = ['some_field']
    page_title = 'All Business Locations'
    add_link = reverse_lazy('businesslocation_add')
    add_perms = 'businesslocation.add_businesslocation'
    edit_url = 'businesslocation_update'
    edit_perms = 'businesslocation.change_businesslocation'
    delete_perms = 'businesslocation.delete_businesslocation'
    delete_url = 'businesslocation_delete'

class BusinessLocationCreateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, CreateView):
    model = BusinessLocation
    form_class = BusinessLocationForm
    template_name = 'add.html'
    success_url = reverse_lazy('businesslocation_list')
    page_title = 'Business Location'
    list_link = reverse_lazy('businesslocation_list')

class BusinessLocationUpdateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, UpdateView):
    model = BusinessLocation
    form_class = BusinessLocationForm
    template_name = 'add.html'
    success_url = reverse_lazy('businesslocation_list')
    page_title = 'Update Business Location'
    list_link = reverse_lazy('businesslocation_list')

class BusinessLocationDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = BusinessLocation
    template_name = 'delete.html'
    page_title = 'Delete Business Location'
    success_url = reverse_lazy('businesslocation_list')



from .models import ExpenseCategory

from .forms import ExpenseCategoryForm

from .tables import ExpenseCategoryTable

from .filters import ExpenseCategoryFilter

class ExpenseCategoryListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = ExpenseCategory
    table_class = ExpenseCategoryTable
    template_name = 'list.html'
    filterset_class = ExpenseCategoryFilter
    #ordering = ['some_field']
    page_title = 'All ExpenseCategorys'
    add_link = reverse_lazy('expensecategory_add')
    add_perms = 'expensecategory.add_expensecategory'
    edit_url = 'expensecategory_update'
    edit_perms = 'expensecategory.change_expensecategory'
    delete_perms = 'expensecategory.delete_expensecategory'
    delete_url = 'expensecategory_delete'

class ExpenseCategoryCreateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = 'add.html'
    success_url = reverse_lazy('expensecategory_list')
    page_title = 'ExpenseCategory'
    list_link = reverse_lazy('expensecategory_list')

class ExpenseCategoryUpdateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = 'add.html'
    success_url = reverse_lazy('expensecategory_list')
    page_title = 'Update ExpenseCategory'
    list_link = reverse_lazy('expensecategory_list')

class ExpenseCategoryDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = ExpenseCategory
    template_name = 'delete.html'
    page_title = 'Delete ExpenseCategory'
    success_url = reverse_lazy('expensecategory_list')

from .models import PaymentAccount

from .forms import PaymentAccountForm

from .tables import PaymentAccountTable

from .filters import PaymentAccountFilter

class PaymentAccountListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = PaymentAccount
    table_class = PaymentAccountTable
    template_name = 'list.html'
    filterset_class = PaymentAccountFilter
    #ordering = ['some_field']
    page_title = 'All PaymentAccounts'
    add_link = reverse_lazy('paymentaccount_add')
    add_perms = 'paymentaccount.add_paymentaccount'
    edit_url = 'paymentaccount_update'
    edit_perms = 'paymentaccount.change_paymentaccount'
    delete_perms = 'paymentaccount.delete_paymentaccount'
    delete_url = 'paymentaccount_delete'

class PaymentAccountCreateView(LoginRequiredMixin, PageHeaderMixin, MessageMixin,CreateView):
    model = PaymentAccount
    form_class = PaymentAccountForm
    template_name = 'add.html'
    success_url = reverse_lazy('paymentaccount_list')
    page_title = 'PaymentAccount'
    list_link = reverse_lazy('paymentaccount_list')

class PaymentAccountUpdateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, UpdateView):
    model = PaymentAccount
    form_class = PaymentAccountForm
    template_name = 'add.html'
    success_url = reverse_lazy('paymentaccount_list')
    page_title = 'Update PaymentAccount'
    list_link = reverse_lazy('paymentaccount_list')

class PaymentAccountDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = PaymentAccount
    template_name = 'delete.html'
    page_title = 'Delete PaymentAccount'
    success_url = reverse_lazy('paymentaccount_list')

from .models import FundTransfer

from .forms import FundTransferForm

from .tables import FundTransferTable

from .filters import FundTransferFilter

class FundTransferListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = FundTransfer
    table_class = FundTransferTable
    template_name = 'list.html'
    filterset_class = FundTransferFilter
    #ordering = ['some_field']
    page_title = 'All FundTransfers'
    add_link = reverse_lazy('fundtransfer_add')
    add_perms = 'fundtransfer.add_fundtransfer'
    # edit_url = 'fundtransfer_update'
    # edit_perms = 'fundtransfer.change_fundtransfer'
    # delete_perms = 'fundtransfer.delete_fundtransfer'
    # delete_url = 'fundtransfer_delete'

class FundTransferCreateView(LoginRequiredMixin, PageHeaderMixin, MessageMixin,CreateView):
    model = FundTransfer
    form_class = FundTransferForm
    template_name = 'add.html'
    success_url = reverse_lazy('fundtransfer_list')
    page_title = 'FundTransfer'
    list_link = reverse_lazy('fundtransfer_list')

class FundTransferUpdateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, UpdateView):
    model = FundTransfer
    form_class = FundTransferForm
    template_name = 'add.html'
    success_url = reverse_lazy('fundtransfer_list')
    page_title = 'Update FundTransfer'
    list_link = reverse_lazy('fundtransfer_list')

class FundTransferDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = FundTransfer
    template_name = 'delete.html'
    page_title = 'Delete FundTransfer'
    success_url = reverse_lazy('fundtransfer_list')

from .forms import ExpenseForm

from .tables import ExpenseTable

from .filters import ExpenseFilter

class ExpenseListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Expense
    table_class = ExpenseTable
    template_name = 'expence_list.html'
    filterset_class = ExpenseFilter
    #ordering = ['some_field']
    page_title = 'All Expenses'
    add_link = reverse_lazy('expense_add')
    add_perms = 'expense.add_expense'
    edit_url = 'expense_update'
    edit_perms = 'expense.change_expense'
    delete_perms = 'expense.delete_expense'
    delete_url = 'expense_delete'

class ExpenseCreateView(LoginRequiredMixin, PageHeaderMixin, MessageMixin,CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'add.html'
    success_url = reverse_lazy('expense_list')
    page_title = 'Expense'
    list_link = reverse_lazy('expense_list')

class ExpenseDetailsModalView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expense_details_modal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related payments to the context
        context['payments'] = self.object.payments.all()
        return context
    
class ExpenseUpdateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'add.html'
    success_url = reverse_lazy('expense_list')
    page_title = 'Update Expense'
    list_link = reverse_lazy('expense_list')

class ExpenseDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = Expense
    template_name = 'delete.html'
    page_title = 'Delete Expense'
    success_url = reverse_lazy('expense_list')

from .models import ExpensePayment

from .forms import ExpensePaymentForm

from .tables import ExpensePaymentTable

from .filters import ExpensePaymentFilter

class ExpensePaymentListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = ExpensePayment
    table_class = ExpensePaymentTable
    template_name = 'list.html'
    filterset_class = ExpensePaymentFilter
    #ordering = ['some_field']
    page_title = 'All ExpensePayments'
    add_link = reverse_lazy('expensepayment_add')
    add_perms = 'expensepayment.add_expensepayment'
    edit_url = 'expensepayment_update'
    edit_perms = 'expensepayment.change_expensepayment'
    delete_perms = 'expensepayment.delete_expensepayment'
    delete_url = 'expensepayment_delete'

class ExpensePaymentCreateView(LoginRequiredMixin, PageHeaderMixin, MessageMixin ,CreateView):
    model = ExpensePayment
    form_class = ExpensePaymentGeneralForm
    template_name = 'add.html'
    success_url = reverse_lazy('expensepayment_list')
    page_title = 'ExpensePayment'
    list_link = reverse_lazy('expensepayment_list')
    

class ExpensePaymentCreateByIDView(LoginRequiredMixin,MessageMixin, CreateView):
    model = ExpensePayment
    form_class = ExpensePaymentForm
    template_name = 'add.html'
    success_url = reverse_lazy('expensepayment_list')  # Update this to the appropriate URL

    def dispatch(self, request, *args, **kwargs):
        """
        Ensure the expense has a remaining balance before proceeding.
        """
        expense_id = self.kwargs.get('expense_id')
        expense = get_object_or_404(Expense, pk=expense_id)

        if expense.remaining_balance <= 0:
            messages.error(request, f"The expense '{expense}' is already fully paid.")
            return redirect(self.success_url)  # Redirect to the expense payment list or detail page

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Prepopulate the 'expense' field with the specific expense.
        """
        expense_id = self.kwargs.get('expense_id')
        expense = get_object_or_404(Expense, pk=expense_id)
        return {'expense': expense}

    def get_form_kwargs(self):
        """
        Pass the specific expense to the form instance.
        """
        kwargs = super().get_form_kwargs()
        expense_id = self.kwargs.get('expense_id')
        expense = get_object_or_404(Expense, pk=expense_id)
        kwargs['initial'] = {'expense': expense}
        kwargs['expense_instance'] = expense  # Pass the expense instance to the form
        return kwargs

    def form_valid(self, form):
        """
        Save the form and handle cases where there are no prior payments.
        """
        expense_id = self.kwargs.get('expense_id')
        expense = get_object_or_404(Expense, pk=expense_id)
        form.instance.expense = expense

        # Ensure that payment amount does not exceed the remaining balance
        if form.cleaned_data['amount'] > expense.remaining_balance:
            form.add_error('amount', f"Payment amount cannot exceed the remaining balance of {expense.remaining_balance}.")
            return self.form_invalid(form)

        messages.success(self.request, 'Payment added successfully!.')
        return super().form_valid(form)


class ExpensePaymentUpdateView(LoginRequiredMixin, PageHeaderMixin,MessageMixin, UpdateView):
    model = ExpensePayment
    form_class = ExpensePaymentForm
    template_name = 'add.html'
    success_url = reverse_lazy('expensepayment_list')
    page_title = 'Update ExpensePayment'
    list_link = reverse_lazy('expensepayment_list')

class ExpensePaymentDeleteView(LoginRequiredMixin, PageHeaderMixin, MessageMixin,DeleteView):
    model = ExpensePayment
    template_name = 'delete.html'
    page_title = 'Delete ExpensePayment'
    success_url = reverse_lazy('expensepayment_list')

from .models import PaymentAccountDeposit

from .forms import PaymentAccountDepositForm

from .tables import PaymentAccountDepositTable

from .filters import PaymentAccountDepositFilter

class PaymentAccountDepositListView(PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = PaymentAccountDeposit
    table_class = PaymentAccountDepositTable
    template_name = 'list.html'
    filterset_class = PaymentAccountDepositFilter
    #ordering = ['some_field']
    page_title = 'All Payment Account Deposit'
    add_link = reverse_lazy('paymentaccountdeposit_add')
    add_perms = 'paymentaccountdeposit.add_paymentaccountdeposit'
    # edit_url = 'paymentaccountdeposit_update'
    # edit_perms = 'paymentaccountdeposit.change_paymentaccountdeposit'
    # delete_perms = 'paymentaccountdeposit.delete_paymentaccountdeposit'
    # delete_url = 'paymentaccountdeposit_delete'

class PaymentAccountDepositCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = PaymentAccountDeposit
    form_class = PaymentAccountDepositForm
    template_name = 'add.html'
    success_url = reverse_lazy('paymentaccountdeposit_list')
    page_title = 'PaymentAccountDeposit'
    list_link = reverse_lazy('paymentaccountdeposit_list')

# class PaymentAccountDepositUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
#     model = PaymentAccountDeposit
#     form_class = PaymentAccountDepositForm
#     template_name = 'add.html'
#     success_url = reverse_lazy('paymentaccountdeposit_list')
#     page_title = 'Update PaymentAccountDeposit'
#     list_link = reverse_lazy('paymentaccountdeposit_list')

# class PaymentAccountDepositDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
#     model = PaymentAccountDeposit
#     template_name = 'delete.html'
#     page_title = 'Delete PaymentAccountDeposit'
#     success_url = reverse_lazy('paymentaccountdeposit_list')
