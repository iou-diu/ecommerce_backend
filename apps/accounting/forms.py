from django import forms
from django.db.models import F, Sum
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from django.utils.safestring import mark_safe

from crispy_forms.layout import Layout, Row, Column, HTML, Submit,Fieldset

from apps.accounting.lookup import AccountSelect2Widget
from .models import Account, AccountHead, Bill, Expense, Payment, Transaction, TransactionLine

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['head', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('head', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
            ),
        )

class TransactionLineForm(forms.ModelForm):
    class Meta:
        model = TransactionLine
        fields = ['account', 'transaction_type', 'amount']
        exclude = ('id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('account', css_class='form-group col-md-4 mb-0'),
                Column('transaction_type', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
            ),
        )

TransactionLineFormSet = inlineformset_factory(
    Transaction, TransactionLine, form=TransactionLineForm,
    extra=1, can_delete=True
)





class AccountHeadForm(forms.ModelForm):
    class Meta:
        model = AccountHead
        fields = ('name', 'head_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'head_type'),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary', 
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class AccountHeadFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('head_type', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'account_type', 'account_head', 'opening_balance', 'closing_balance', 'current_balance', 'is_closed',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'account_type', 'account_head', 'opening_balance', 'closing_balance', 'current_balance', 'is_closed'),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary', 
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class AccountFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('account_type', css_class='form-group col-md-4 mb-0'),
                Column('account_head', css_class='form-group col-md-4 mb-0'),
                Column('opening_balance', css_class='form-group col-md-4 mb-0'),
                Column('closing_balance', css_class='form-group col-md-4 mb-0'),
                Column('current_balance', css_class='form-group col-md-4 mb-0'),
                Column('is_closed', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('description', 'head',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adjust the 'description' field's widget to have 2 rows
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 2})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('head', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
               
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary', 
                           onclick="return confirm('Are you sure you want to submit?');"),
                    css_class='text-right'  # Align the button to the right if desired
                ),
            )
        )

class TransactionFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('description', css_class='form-group col-md-4 mb-0'),
                Column('head', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )



class TransactionLineForm(forms.ModelForm):
    class Meta:
        model = TransactionLine
        fields = ['account', 'transaction_type', 'amount']
        widgets = {
            'account': AccountSelect2Widget(attrs={
                'data-minimum-input-length': 0,
            }),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransactionLineFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('transaction', css_class='form-group col-md-4 mb-0'),
                Column('account', css_class='form-group col-md-4 mb-0'),
                Column('transaction_type', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )



# double entry 
class BaseTransactionLineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_debit = 0
        total_credit = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                amount = form.cleaned_data.get('amount', 0)
                transaction_type = form.cleaned_data.get('transaction_type')
                if transaction_type == 'debit':
                    total_debit += amount
                elif transaction_type == 'credit':
                    total_credit += amount
        if total_debit != total_credit:
            raise forms.ValidationError('Total debits and credits must balance.')

TransactionLineFormSetNew = inlineformset_factory(
    Transaction,
    TransactionLine,
    form=TransactionLineForm,
    formset=BaseTransactionLineFormSet,
    extra=2,  # Adjust 'extra' to show the number of forms you need by default
    can_delete=False  # Set to True if you want to allow deletion
)




# bill payments section

class CompleteBillForm(forms.ModelForm):
    credit_account = forms.ModelChoiceField(
        queryset=Account.objects.filter(account_type='revenue'),  # Filter only credit accounts
        required=True,
        label="Credit Account"
    )

    enable_payment = forms.BooleanField(
        required=False, label="Add Payment"
    )
    payment_amount = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, label="Payment Amount"
    )

    class Meta:
        model = Bill
        fields = ['user', 'due_date', 'total_amount', 'credit_account','enable_payment', 'payment_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ensure 'due_date' is shown as a date input
        

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('credit_account', css_class='form-group col-md-6 mb-0'),
                Column('user', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                
                Column('due_date', css_class='form-group col-md-6 mb-0'),
                Column('total_amount', css_class='form-group col-md-6 mb-0'),
            ),
             Row(
                Column('enable_payment', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('payment_amount', css_class='form-group col-md-6 mb-0', id="payment_amount_row"),
            ),
            
            Row(
                Column(
                    Submit('submit', 'Create Fee'),
                    css_class='text-right'
                ),
            )
        )


class CompletePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['bill', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Make Payment'))

        # Limit bill choices to unpaid or partially paid bills
        self.fields['bill'].queryset = Bill.objects.filter(
            status__in=[Bill.Status.UNPAID, Bill.Status.PARTIALLY_PAID]
        )

    def clean(self):
        cleaned_data = super().clean()
        bill = cleaned_data.get('bill')
        amount = cleaned_data.get('amount')

        if bill and amount:
            if amount > bill.total_due:
                raise forms.ValidationError(f"Payment amount cannot exceed the remaining due amount of {bill.total_due}")

        return cleaned_data


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('user',  'due_date', 'total_amount', 'total_paid', 'total_due', 'status', 'transaction',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user',  'due_date', 'total_amount', 'total_paid', 'total_due', 'status', 'transaction'),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary', 
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class BillFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-4 mb-0'),
                Column('billing_date', css_class='form-group col-md-4 mb-0'),
                Column('due_date', css_class='form-group col-md-4 mb-0'),
                Column('total_amount', css_class='form-group col-md-4 mb-0'),
                Column('total_paid', css_class='form-group col-md-4 mb-0'),
                Column('total_due', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('transaction', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('user', 'bill', 'amount',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user', 'bill', 'amount',),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary', 
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class PaymentFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-4 mb-0'),
                Column('bill', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
                Column('payment_date', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

from .models import BusinessLocation

class BusinessLocationForm(forms.ModelForm):
    class Meta:
        model = BusinessLocation
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name'),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary',               onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class BusinessLocationFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

from .models import ExpenseCategory

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ('name', 'parent_category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'parent_category'),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary',               onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class ExpenseCategoryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('parent_category', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

from .models import PaymentAccount

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = PaymentAccount
        fields = ('name', 'opening_balance', 'current_balance', 'account_type', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'opening_balance', 'current_balance', 'account_type', 'is_active'),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary',               onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class PaymentAccountFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('opening_balance', css_class='form-group col-md-4 mb-0'),
                Column('current_balance', css_class='form-group col-md-4 mb-0'),
                Column('account_type', css_class='form-group col-md-4 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

from .models import FundTransfer

class FundTransferForm(forms.ModelForm):
    class Meta:
        model = FundTransfer
        fields = ('from_account', 'to_account', 'amount', 'document', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize help texts and widgets for better usability
        self.fields['from_account'].label = "From Account"
        self.fields['to_account'].label = "To Account"
        self.fields['amount'].label = "Transfer Amount"
        self.fields['document'].label = "Attachment"
        self.fields['note'].label = "Transfer Note"

        self.fields['amount'].widget.attrs.update({'placeholder': 'Enter amount to transfer'})
        self.fields['note'].widget.attrs.update({'placeholder': 'Optional: Add any notes about the transfer'})

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Fieldset(
                "Fund Transfer Details",
                Row(
                    Column('from_account', css_class='form-group col-md-6 mb-3'),
                    Column('to_account', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('amount', css_class='form-group col-md-6 mb-3'),
                    Column('document', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('note', css_class='form-group col-md-12 mb-3'),
                ),
            ),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-primary'),
                HTML(
                    "<a class='btn btn-secondary' href='{% url \"fundtransfer_list\" %}'>Cancel</a>"
                ),
            ),
        )

class FundTransferFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('from_account', css_class='form-group col-md-4 mb-0'),
                Column('to_account', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
                
                Column('note', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )



class ExpenseForm(forms.ModelForm):
    add_payment = forms.BooleanField(
        required=False,
        initial=False,
        label="Add Payment",
        help_text="Check this box to add payment details for the expense."
    )
    payment_account = forms.ModelChoiceField(
        queryset=None,  # Dynamically set in `__init__`
        required=False,
        label="Payment Account",
        help_text="Select the account to debit for this payment."
    )
    payment_amount = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Payment Amount",
        help_text="Enter the amount to be paid immediately for this expense."
    )
    payment_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Payment Note",
        help_text="Add a note for the payment, if needed."
    )

    class Meta:
        model = Expense
        fields = [
            'business_location', 'category', 'reference_no', 'document', 'expense_for',
            'contact', 'applicable_tax', 'total_amount', 'expense_note', 'is_recurring',
            'recurring_interval', 'interval_type', 'no_of_repetitions', 'repeat_on'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic queryset for payment accounts
        from .models import PaymentAccount  # Import here to avoid circular imports
        self.fields['payment_account'].queryset = PaymentAccount.objects.filter(is_active=True)
        
        # Add Crispy Forms helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('business_location', css_class='form-group col-md-6'),
                Column('category', css_class='form-group col-md-6'),
            ),
            Row(
                Column('reference_no', css_class='form-group col-md-6'),
                Column('document', css_class='form-group col-md-6'),
            ),
            Row(
                Column('expense_for', css_class='form-group col-md-6'),
                Column('contact', css_class='form-group col-md-6'),
            ),
            Row(
                Column('applicable_tax', css_class='form-group col-md-6'),
                Column('total_amount', css_class='form-group col-md-6'),
            ),
            Row(
                Column('expense_note', css_class='form-group col-md-12'),
            ),
            Row(
                Column('is_recurring', css_class='form-group col-md-4'),
                Column('recurring_interval', css_class='form-group col-md-4'),
                Column('interval_type', css_class='form-group col-md-4'),
            ),
            Row(
                Column('no_of_repetitions', css_class='form-group col-md-6'),
                Column('repeat_on', css_class='form-group col-md-6'),
            ),
            Row(
                Column('add_payment', css_class='form-group col-md-12'),
            ),
            Row(
                Column('payment_account', css_class='form-group col-md-6'),
                Column('payment_amount', css_class='form-group col-md-6'),
            ),
            Row(
                Column('payment_note', css_class='form-group col-md-12'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            ),
        )

    def clean(self):
        """
        Custom validation for payment fields.
        """
        cleaned_data = super().clean()
        add_payment = cleaned_data.get('add_payment')
        payment_account = cleaned_data.get('payment_account')
        payment_amount = cleaned_data.get('payment_amount')

        if add_payment:
            if not payment_account:
                raise forms.ValidationError("Payment account is required when adding a payment.")
            if not payment_amount or payment_amount <= 0:
                raise forms.ValidationError("Valid payment amount is required.")
            if payment_amount > self.instance.remaining_balance:
                raise forms.ValidationError(
                    f"Payment amount ({payment_amount}) exceeds the remaining balance ({self.instance.remaining_balance})."
                )
        return cleaned_data

    def save(self, *args, **kwargs):
        """
        Save Expense and optionally create ExpensePayment.
        """
        expense = super().save(*args, **kwargs)

        # Handle payment creation if add_payment is checked
        if self.cleaned_data.get('add_payment'):
            ExpensePayment.objects.create(
                expense=expense,
                payment_account=self.cleaned_data['payment_account'],
                amount=self.cleaned_data['payment_amount'],
                note=self.cleaned_data['payment_note'],
            )
        return expense
    


class ExpenseFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('business_location', css_class='form-group col-md-4 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('reference_no', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-4 mb-0'),
               
                Column('expense_for', css_class='form-group col-md-4 mb-0'),
                Column('contact', css_class='form-group col-md-4 mb-0'),
                
                Column('is_recurring', css_class='form-group col-md-4 mb-0'),
               

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

from .models import ExpensePayment

class ExpensePaymentForm(forms.ModelForm):
    class Meta:
        model = ExpensePayment
        fields = ('expense', 'payment_account', 'amount', 'note')

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and handle dynamic fields, including 
        displaying helpful information about the selected expense.
        """
        expense_instance = kwargs.pop('expense_instance', None)
        super().__init__(*args, **kwargs)

        # Queryset for the expense field to include only expenses with remaining balances
        self.fields['expense'].queryset = Expense.objects.annotate(
            remaining_balance=F('total_amount') - Sum('payments__amount')
        ).filter(remaining_balance__gt=0)

        # Restrict the expense queryset if an instance is passed
        if expense_instance:
            self.fields['expense'].queryset = Expense.objects.filter(pk=expense_instance.pk)

        # Queryset for payment accounts
        self.fields['payment_account'].queryset = PaymentAccount.objects.filter(is_active=True)

        # Add Crispy Form Helper for styling
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('expense', css_class='form-group col-md-6 mb-0'),
                Column('payment_account', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('amount', css_class='form-group col-md-6 mb-0'),
                Column('note', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary'),
                    css_class='form-group col-md-12 text-right',
                )
            )
        )

    def clean(self):
        """
        Custom validation to ensure payment is valid and doesn't exceed the remaining balance.
        """
        cleaned_data = super().clean()
        expense = cleaned_data.get('expense')
        payment_account = cleaned_data.get('payment_account')
        amount = cleaned_data.get('amount')

        if not expense:
            raise forms.ValidationError("Please select a valid expense.")

    

        if amount is None or amount <= 0:
            raise forms.ValidationError("Payment amount must be greater than zero.")

        

        if not payment_account:
            raise forms.ValidationError("Please select a valid payment account.")

        return cleaned_data

    def save(self, commit=True):
        """
        Override save to handle additional logic for payments, such as marking the expense status.
        """
        instance = super().save(commit=False)

        # Update the expense's remaining balance and status
        remaining_balance = instance.expense.total_amount - (
            instance.expense.payments.aggregate(Sum('amount'))['amount__sum'] or 0
        ) - instance.amount

        if remaining_balance == 0:
            instance.expense.status = "paid"
        elif remaining_balance < instance.expense.total_amount:
            instance.expense.status = "partially_paid"
        else:
            instance.expense.status = "due"

        instance.expense.save()

        if commit:
            instance.save()
        return instance


class ExpensePaymentGeneralForm(forms.ModelForm):
    class Meta:
        model = ExpensePayment
        fields = ('expense', 'payment_account', 'amount', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter expenses to include only those with a remaining balance greater than 0
        self.fields['expense'].queryset = Expense.objects.exclude(status='paid')

        # Filter active payment accounts
        self.fields['payment_account'].queryset = PaymentAccount.objects.filter(is_active=True)

        # Add Crispy Forms layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('expense', css_class='col-md-6'),
                Column('payment_account', css_class='col-md-6'),
            ),
            Row(
                Column('amount', css_class='col-md-6'),
                Column('note', css_class='col-md-6'),
            ),
            Row(
                Submit('submit', 'Save', css_class='btn btn-primary'),
            ),
        )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Payment amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        expense = cleaned_data.get('expense')
        amount = cleaned_data.get('amount')

        if expense:
            remaining_balance = expense.total_amount - sum(
                expense.payments.values_list('amount', flat=True)
            )
            if amount > remaining_balance:
                raise forms.ValidationError(
                    f"Payment amount ({amount}) exceeds the remaining balance ({remaining_balance})."
                )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Automatically update the expense status based on the payment
        remaining_balance = instance.expense.total_amount - (
            instance.expense.payments.aggregate(Sum('amount'))['amount__sum'] or 0
        ) - instance.amount

        if remaining_balance == 0:
            instance.expense.status = "paid"
        elif remaining_balance < instance.expense.total_amount:
            instance.expense.status = "partially_paid"
        else:
            instance.expense.status = "due"

        instance.expense.save()

        if commit:
            instance.save()
        return instance

class ExpensePaymentFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('expense', css_class='form-group col-md-4 mb-0'),
                Column('payment_account', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
                Column('payment_date', css_class='form-group col-md-4 mb-0'),
                Column('note', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )

from .models import PaymentAccountDeposit

class PaymentAccountDepositForm(forms.ModelForm):
    class Meta:
        model = PaymentAccountDeposit
        fields = ('payment_account', 'amount', 'deposit_date', 'notes', 'document',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('payment_account', 'amount', 'deposit_date', 'notes', 'document',),
            ),
            Row(
                Column(
                   Submit('submit', 'Save', css_class='btn btn-primary',               onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

class PaymentAccountDepositFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('payment_account', css_class='form-group col-md-4 mb-0'),
             
                Column('deposit_date', css_class='form-group col-md-4 mb-0'),
             
                Column('created_at', css_class='form-group col-md-4 mb-0'),
                Column('updated_at', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )
