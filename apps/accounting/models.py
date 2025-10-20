from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.ecom.models import Tax
from apps.user.models import CustomUser

class AccountHead(models.Model):
    HEAD_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=255)
    head_type = models.CharField(max_length=50, choices=HEAD_TYPES)

    def __str__(self):
        return f"{self.name} ({self.get_head_type_display()})"


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    account_head = models.ForeignKey(AccountHead, on_delete=models.CASCADE, related_name='accounts')  # Correct relation to AccountHead
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    closing_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_closed = models.BooleanField(default=False)

    @property
    def total_balance(self):
        return self.opening_balance + self.current_balance
    
    def update_closing_balance(self):
        self.closing_balance = self.current_balance
        self.save()

    def settle_balance(self):
        if self.current_balance != 0:
            # Example: Handle balance transfer to another account
            pass
        self.current_balance = 0
        self.save()

    def close_account(self):
        self.settle_balance()
        self.update_closing_balance()
        self.is_closed = True
        self.save()

    def reopen_account(self):
        self.is_closed = False
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"


class Transaction(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    head = models.ForeignKey(AccountHead, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transaction on {self.date} - {self.description} under {self.head.name}"


class TransactionLine(models.Model):
    TRANSACTION_TYPES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]
    
    transaction = models.ForeignKey(Transaction, related_name='lines', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)  

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only apply logic for new transaction lines
            if self.account.account_type in ['asset', 'expense']:
                if self.transaction_type == 'debit':
                    self.account.current_balance += self.amount  # Debit increases asset/expense
                elif self.transaction_type == 'credit':
                    if self.account.current_balance < self.amount:
                        raise ValueError("Insufficient balance for this credit transaction.")
                    self.account.current_balance -= self.amount  # Credit decreases asset/expense
            elif self.account.account_type in ['liability', 'equity', 'revenue']:
                print("revenue paisi")
                if self.transaction_type == 'debit':
                    if self.account.current_balance < self.amount:
                        raise ValueError("Insufficient balance for this debit transaction.")
                    self.account.current_balance -= self.amount  # Debit decreases liability/equity/revenue
                elif self.transaction_type == 'credit':
                    self.account.current_balance += self.amount  # Credit increases liability/equity/revenue

            # Save the updated account balance
            self.account.save()

        # Call the parent class's save method to save the TransactionLine
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} {self.amount} to {self.account.name}"


    # def save(self, *args, **kwargs):
    #     # Apply debit/credit logic to update the account's current balance
    #     if self.pk is None:  # Only apply logic for new transaction lines
    #         if self.account.account_type in ['asset', 'expense']:
    #             if self.transaction_type == 'debit':
    #                 self.account.current_balance += self.amount  # Debit increases asset/expense
    #             elif self.transaction_type == 'credit':
    #                 self.account.current_balance -= self.amount  # Credit decreases asset/expense
    #         elif self.account.account_type in ['liability', 'equity', 'revenue']:
    #             if self.transaction_type == 'debit':
    #                 self.account.current_balance -= self.amount  # Debit decreases liability/equity/revenue
    #             elif self.transaction_type == 'credit':
    #                 self.account.current_balance += self.amount  # Credit increases liability/equity/revenue

    #         # Save the updated account balance
    #         self.account.save()

    #     # Call the parent class's save method to save the TransactionLine
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} {self.amount} to {self.account.name}"
    

# single bill or multi seperate payments? 

class Bill(models.Model):

    class Status(models.TextChoices):
        UNPAID = 'unpaid', 'Unpaid'
        PARTIALLY_PAID = 'partially_paid', 'Partially Paid'
        PAID = 'paid', 'Paid'
        REJECTED = 'rejected', 'Rejected'

    user = models.CharField(max_length=255) # later foreign key
    billing_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_due = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,  # Use the choices from the TextChoices class
        default=Status.UNPAID  # Set a default status
    )
    transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.SET_NULL)  # Linked transaction


    def __str__(self):
        return f"Bills due {self.due_date} with total due {self.total_due}"

class BillLine(models.Model):
    bill = models.ForeignKey(Bill, related_name='bill_lines', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount}"
    
    
class Payment(models.Model):
    user = models.CharField(max_length=255) # later foreign key
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Payment of {self.amount} for Bill {self.bill.id}"
    

# fines will be added as bill 
# bill lines or at a time all heads


# expanse sales cogs (purchase order e cogs)

class BusinessLocation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories"
    )  # Self-referential ForeignKey for hierarchical structure

    def __str__(self):
        if self.parent_category:
            return f"{self.parent_category.name} > {self.name}"  # Parent > Subcategory
        return self.name

    
class Expense(models.Model):
    REPEAT_CHOICES = [
        ("1st", "1st Day of Month"),
        ("15th", "15th Day of Month"),
        ("end_of_month", "End of Month"),
    ]

    STATUS_CHOICES = [
        ("due", "Due"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    business_location = models.ForeignKey(BusinessLocation, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to="expenses/documents/", null=True, blank=True)
    expense_for = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="expense_for_staff",
        limit_choices_to={"groups__name__in": ["Admin", "Staff"]}  # Limit to Admins and Staff
    )
    contact = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="expense_contact",
        limit_choices_to={"groups__name": "Customer"}  # Limit to Customers
    )
    applicable_tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_note = models.TextField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurring_interval = models.PositiveIntegerField(blank=True, null=True)
    interval_type = models.CharField(
        max_length=50, choices=[("days", "Days"), ("months", "Months")], blank=True, null=True
    )
    no_of_repetitions = models.PositiveIntegerField(blank=True, null=True)
    repeat_on = models.CharField(
        max_length=20, choices=REPEAT_CHOICES, blank=True, null=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="due"
    ) 

    @property
    def total_payments(self):
        """
        Calculate the total payments made for this expense.
        """
        if not self.pk:
            return Decimal("0.00")  # Return 0 if the instance is not saved yet
        return self.payments.aggregate(total=models.Sum("amount"))["total"] or Decimal("0.00")
    
    @property
    def remaining_balance(self):
        """
        Calculate the remaining balance for the expense.
        """
        if not self.pk:
            return self.total_amount  # Return total amount if instance is not saved yet
        return self.total_amount - self.total_payments
    
    def __str__(self):
        return f"Expense {self.reference_no or self.id} - Total {self.total_amount}  Due {self.remaining_balance}"

    
    def update_status(self):
        """
        Dynamically update the status of the expense based on the remaining balance.
        """
        if not self.pk:
            return
        if self.remaining_balance == self.total_amount:
            self.status = "due"
        elif self.remaining_balance > 0:
            self.status = "partially_paid"
        elif self.remaining_balance == 0:
            self.status = "paid"

    def clean(self):
        """Custom validation logic for expense_for and contact fields."""
        if self.expense_for:
            if not self.expense_for.groups.filter(name__in=["Admin", "Staff"]).exists():
                raise ValidationError("Expense For must be assigned to an Admin or Staff user.")

        if self.contact:
            if not self.contact.groups.filter(name="Customer").exists():
                raise ValidationError("Contact must be assigned to a Customer user.")
            
        if self.is_recurring and not self.recurring_interval:
            raise ValidationError("Recurring interval is required for recurring expenses.")
        if self.is_recurring and not self.repeat_on:
            raise ValidationError("Repeat On is required for recurring expenses.")

    def save(self, *args, **kwargs):
        """Override save method to perform custom validation."""
        self.full_clean()  # Run the clean method before saving
        if not self.pk:
            super().save(*args, **kwargs)
            
        self.update_status() 
        super().save(*args, **kwargs)






class PaymentAccount(models.Model):
    name = models.CharField(max_length=100)  # Account name, e.g., Bank, Cash
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_type = models.CharField(
        max_length=50,
        choices=[
            ("bank", "Bank"),
            ("cash", "Cash"),
            ("credit", "Credit"),
            ("mfs", "MFS"),
        ],
        default="bank",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Order creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp

    def __str__(self):
        return f"{self.name} (Balance: {self.current_balance})"

    def update_balance(self, amount, transaction_type):
        """
        Update the current balance based on transaction type.
        """
        if transaction_type == "debit":  # Deduct amount
            self.current_balance -= amount
        elif transaction_type == "credit":  # Add amount
            self.current_balance += amount
        self.save()

class PaymentAccountDeposit(models.Model):
    payment_account = models.ForeignKey(
        PaymentAccount, 
        on_delete=models.CASCADE, 
        related_name="deposits"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to="deposits/documents/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Deposit of {self.amount} to {self.payment_account.name}"

    def save(self, *args, **kwargs):
        """
        Override save to:
        1. Update the PaymentAccount's current_balance (credit).
        2. Save the deposit record.
        """
        # If deposit is new (i.e., no primary key yet),
        # then increase the PaymentAccount's balance
        is_new = self.pk is None  
        super().save(*args, **kwargs)
        
        if is_new:
            self.payment_account.update_balance(self.amount, transaction_type="credit")

class ExpensePayment(models.Model):
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name="payments"
    )
    payment_account = models.ForeignKey(
        PaymentAccount, on_delete=models.CASCADE, related_name="expense_payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Expense {self.expense.id} - {self.amount}"

    def clean(self):
        """
        Validate payment amount does not exceed remaining balance.
        """
        remaining_balance = self.expense.remaining_balance
        if self.amount > remaining_balance:
            raise ValidationError(
                f"Payment amount ({self.amount}) exceeds remaining balance ({remaining_balance})."
            )
            
        if self.amount > self.payment_account.current_balance:
            raise ValidationError(
                f"Payment account '{self.payment_account.name}' does not have sufficient funds. "
                "Please deposit or transfer funds to proceed with this payment."
            )


    def save(self, *args, **kwargs):
        """
        Override save to update the PaymentAccount balance.
        """

        self.full_clean()


        if not self.pk:  # If it's a new payment
            self.payment_account.update_balance(self.amount, "debit")
        super().save(*args, **kwargs)

        self.expense.save()


class FundTransfer(models.Model):
    from_account = models.ForeignKey(
        PaymentAccount, on_delete=models.CASCADE, related_name="transfers_out"
    )
    to_account = models.ForeignKey(
        PaymentAccount, on_delete=models.CASCADE, related_name="transfers_in"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to="fund_transfers/documents/", blank=True, null=True)

    created_by  = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="fund_transfers_created",
        limit_choices_to={"groups__name__in": ["Admin", "Staff"]}  # Limit to Admins and Staff
    )


    approved_by  = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="fund_transfers_approved",
        limit_choices_to={"groups__name__in": ["Admin", "Staff"]}  # Limit to Admins and Staff
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Order creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp

    def __str__(self):
        return f"Transfer {self.amount} from {self.from_account} to {self.to_account}"

    def clean(self):
        """
        Custom validation for fund transfer:
        1. Prevent transferring from the same account to itself.
        2. Ensure sufficient balance in the 'from_account'.
        """
        # Check if transferring to the same account
        if self.from_account == self.to_account:
            raise ValidationError("Cannot transfer funds to the same account.")

        # Check if 'from_account' has sufficient balance
        if self.amount > self.from_account.current_balance:
            raise ValidationError(
                f"Insufficient balance in the account '{self.from_account.name}'. "
                f"Available balance: {self.from_account.current_balance}."
            )

    
    def save(self, *args, **kwargs):
        """
        Override save to update balances of both accounts.
        """
        self.full_clean()
        
        with transaction.atomic():
            # Lock both accounts to prevent race conditions
            from_account = PaymentAccount.objects.select_for_update().get(pk=self.from_account.pk)
            to_account = PaymentAccount.objects.select_for_update().get(pk=self.to_account.pk)

            # Check balances again to ensure no changes occurred in a concurrent transaction
            if self.amount > from_account.current_balance:
                raise ValidationError(
                    f"Insufficient balance in the account '{from_account.name}'. "
                    f"Available balance: {from_account.current_balance}."
                )

            # Update balances
            from_account.update_balance(self.amount, "debit")
            to_account.update_balance(self.amount, "credit")

            # Save the transfer record
            super().save(*args, **kwargs)
        
