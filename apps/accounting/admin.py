from django.contrib import admin
from .models import Account, AccountHead, Bill, BusinessLocation, Expense, ExpenseCategory, ExpensePayment, FundTransfer, Payment, PaymentAccount, PaymentAccountDeposit, Transaction, TransactionLine

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'opening_balance', 'closing_balance', 'current_balance', 'total_balance', 'is_closed')
    list_filter = ('account_type', 'is_closed')
    search_fields = ('name',)

@admin.register(AccountHead)
class AccountHeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_type')  # Removed 'related_account'
    list_filter = ('head_type',)
    search_fields = ('name',)

@admin.register(TransactionLine)
class TransactionLineAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'account', 'transaction_type', 'amount', 'date')
    list_filter = ('transaction_type',)
    search_fields = ('transaction__description', 'account__name')

    # def has_change_permission(self, request, obj=None):
    #     if obj:  # If the object exists, disallow editing
    #         return False  # Disable editing
    #     return True  # Allow adding new transactions
    
    # def has_delete_permission(self, request, obj=None):
    #     if obj:  # If the object exists, disallow editing
    #         return False  # Disable editing
    #     return True  # Allow adding new transactions

class TransactionLineInline(admin.TabularInline):
    model = TransactionLine
    extra = 1

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'head')
    list_filter = ('date', 'head')
    search_fields = ('description',)
    # inlines = [TransactionLineInline]

    def has_change_permission(self, request, obj=None):
        if obj:  # If the object exists, disallow editing
            return False  # Disable editing
        return True  # Allow adding new transactions
    


class BillAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_date', 'due_date', 'total_amount', 'total_paid', 'total_due', 'status')
    list_filter = ('status', 'billing_date', 'due_date')  # Filter by status, billing and due dates
    search_fields = ('user',)  # Search by related user fields (username or email)
    date_hierarchy = 'billing_date'  # Adds a drill-down by billing date in the admin
    ordering = ('-billing_date',)  # Orders by latest bills first

    # # Optional: Display related fields for user in admin list
    # def get_user_email(self, obj):
    #     return obj.user.email
    # get_user_email.short_description = 'User Email'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'amount', 'payment_date')
    list_filter = ('payment_date',)  # Filter payments by date
    search_fields = ('bill__user',)  # Search by user's username or email
    date_hierarchy = 'payment_date'  # Adds a drill-down by payment date in the admin
    ordering = ('-payment_date',)  # Orders by latest payments first

    # # Custom function to show related user in payment listing
    # def get_user(self, obj):
    #     return obj.bill.user.username
    # get_user.short_description = 'User'


# Register the models and their admin configurations
admin.site.register(Bill, BillAdmin)
admin.site.register(Payment, PaymentAdmin)


@admin.register(BusinessLocation)
class BusinessLocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent_category")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("business_location", "category", "total_amount", "expense_for", "contact")
    list_filter = ("business_location", "category", "is_recurring")
    search_fields = ("reference_no", "expense_note")
    autocomplete_fields = ("expense_for", "contact")


@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "opening_balance", "current_balance", "account_type", "is_active")
    search_fields = ("name",)

@admin.register(ExpensePayment)
class ExpensePaymentAdmin(admin.ModelAdmin):
    list_display = ("expense", "payment_account", "amount", "payment_date")
    list_filter = ("payment_account",)
    search_fields = ("expense__reference_no",)

@admin.register(FundTransfer)
class FundTransferAdmin(admin.ModelAdmin):
    list_display = ("from_account", "to_account", "amount", "transfer_date")
    search_fields = ("from_account__name", "to_account__name")



admin.site.register(PaymentAccountDeposit)