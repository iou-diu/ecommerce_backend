from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.accounting.models import (
    AccountHead, Account, BusinessLocation, PaymentAccount, 
    ExpenseCategory, Expense, ExpensePayment
)
from apps.user.models import CustomUser

class Command(BaseCommand):
    help = "Seed demo data for the Accounting module display"

    def handle(self, *args, **kwargs):
        # 1. Create Business Locations
        self.stdout.write("Seeding Business Locations...")
        locations = ["Dhaka Main Office", "Uttara Branch Outlet", "Chittagong Warehouse"]
        loc_objs = []
        for loc_name in locations:
            loc, _ = BusinessLocation.objects.get_or_create(name=loc_name)
            loc_objs.append(loc)
        self.stdout.write(self.style.SUCCESS(f"Created {len(loc_objs)} locations."))

        # 2. Create Accounts under already seeded heads
        self.stdout.write("\nSeeding Accounts...")
        bank_head = AccountHead.objects.filter(name="Bank Accounts").first()
        cash_head = AccountHead.objects.filter(name="Cash in Hand").first()
        payable_head = AccountHead.objects.filter(name="Accounts Payable").first()
        
        if bank_head:
            acc, created = Account.objects.get_or_create(
                name="Dutch-Bangla Bank - DBBL",
                account_type="asset",
                account_head=bank_head,
                defaults={"opening_balance": Decimal("150000.50"), "current_balance": Decimal("150000.50")}
            )
            if created: self.stdout.write(self.style.SUCCESS(f"Created Account: {acc.name}"))
            
            acc, created = Account.objects.get_or_create(
                name="Bank Asia - Corporate A/C",
                account_type="asset",
                account_head=bank_head,
                defaults={"opening_balance": Decimal("75000.25"), "current_balance": Decimal("75000.25")}
            )
            if created: self.stdout.write(self.style.SUCCESS(f"Created Account: {acc.name}"))

        if cash_head:
            acc, created = Account.objects.get_or_create(
                name="Main Cash Box",
                account_type="asset",
                account_head=cash_head,
                defaults={"opening_balance": Decimal("12500.00"), "current_balance": Decimal("12500.00")}
            )
            if created: self.stdout.write(self.style.SUCCESS(f"Created Account: {acc.name}"))
            
        if payable_head:
            acc, created = Account.objects.get_or_create(
                name="Payable: Woodwork Supplies Inc.",
                account_type="liability",
                account_head=payable_head,
                defaults={"opening_balance": Decimal("0.00"), "current_balance": Decimal("0.00")}
            )
            if created: self.stdout.write(self.style.SUCCESS(f"Created Account: {acc.name}"))

        # 3. Create Payment Accounts (Where actual spending comes from)
        self.stdout.write("\nSeeding Payment Accounts...")
        pa_cash, _ = PaymentAccount.objects.get_or_create(
            name="Counter Cash (General)",
            account_type="cash",
            defaults={"opening_balance": Decimal("10000.00"), "current_balance": Decimal("10000.00")}
        )
        pa_bank, _ = PaymentAccount.objects.get_or_create(
            name="City Bank - Online Payment",
            account_type="bank",
            defaults={"opening_balance": Decimal("500000.00"), "current_balance": Decimal("500000.00")}
        )
        pa_mfs, _ = PaymentAccount.objects.get_or_create(
            name="bKash Merchant Pay-01",
            account_type="mfs",
            defaults={"opening_balance": Decimal("500.00"), "current_balance": Decimal("500.00")}
        )
        self.stdout.write(self.style.SUCCESS("Created payment accounts for transactions."))

        # 4. Create some Expenses for display in Lists/Dashboards
        self.stdout.write("\nSeeding Demo Expenses & Payments...")
        
        # Ensure a demo admin exists
        user = CustomUser.objects.filter(is_staff=True).first()
        if not user:
            user = CustomUser.objects.create_superuser(
                email="admin@example.com", 
                password="password123", 
                name="Demo Admin"
            )

        # Ensure the user has correct groups based on models.py validation
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        user.groups.add(admin_group, staff_group)

        # Get categories (Created by previous seed_accounting command)
        office_rent = ExpenseCategory.objects.filter(name="Office Rent").first()
        electricity = ExpenseCategory.objects.filter(name="Electricity Bill").first()
        it_support = ExpenseCategory.objects.filter(name="IT Support Services").first()
        
        if office_rent and loc_objs:
            # Fully Paid Expense
            e1 = Expense.objects.create(
                business_location=loc_objs[0],
                category=office_rent,
                reference_no="RENT-APR-2026",
                total_amount=Decimal("55000.00"),
                expense_for=user,
                expense_note="Monthly rent for Dhaka Main Office",
                status="due"
            )
            ExpensePayment.objects.create(
                expense=e1,
                payment_account=pa_bank,
                amount=Decimal("55000.00"),
                note="Rent cleared for April."
            )
            self.stdout.write(self.style.SUCCESS(f"Created PAID Expense: {e1.reference_no}"))

        if electricity and loc_objs:
            # Partially Paid Expense
            e2 = Expense.objects.create(
                business_location=loc_objs[1],
                category=electricity,
                reference_no="UTIL-MAR-001",
                total_amount=Decimal("4500.00"),
                expense_for=user,
                expense_note="Uttara Branch Utility Bill",
                status="due"
            )
            ExpensePayment.objects.create(
                expense=e2,
                payment_account=pa_cash,
                amount=Decimal("2000.00"),
                note="Partial utility payment"
            )
            self.stdout.write(self.style.SUCCESS(f"Created PARTIALLY PAID Expense: {e2.reference_no}"))

        if it_support and loc_objs:
            # Unpaid/Due Expense
            e3 = Expense.objects.create(
                business_location=loc_objs[2],
                category=it_support,
                reference_no="IT-SVC-992",
                total_amount=Decimal("12000.00"),
                expense_for=user,
                expense_note="Quarterly Firewall Maintenance",
                status="due"
            )
            self.stdout.write(self.style.SUCCESS(f"Created DUE Expense: {e3.reference_no}"))

        self.stdout.write(self.style.SUCCESS("\nSuccessfully seeded all Demo Data for Account Module!"))
