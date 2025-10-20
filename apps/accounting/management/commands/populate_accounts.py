from django.core.management.base import BaseCommand

from apps.accounting.models import Account, AccountHead


class Command(BaseCommand):
    help = 'Populate default account heads and accounts'

    def handle(self, *args, **kwargs):
        # Define account heads and accounts
        account_data = {
            'Asset': [
                'Cash',
                'Bank',
                'Accounts Receivable',
                'Inventory',
                'Prepaid Expenses',
            ],
            'Liability': [
                'Accounts Payable',
                'Accrued Liabilities',
                'Unearned Revenue',
                'Loans Payable',
                'Taxes Payable',
                'Security Money',
            ],
            'Equity': [
                'Owner\'s Capital',
                'Retained Earnings',
            ],
            'Revenue': [
                'Sales Revenue',
                'Service Revenue',
                'Interest Income',
                'Rent Income',
                'Auditorium/Conference Room Rent',
                'Certificate Fee/Recruitment Income',
                'Library Development Fee',
                'Others',
                'Delay Fine',
            ],
            'Expense': [
                'Cost of Goods Sold',
                'Salary Expense',
                'Rent Expense',
                'Utilities Expense',
                'Depreciation Expense',
                'Salary Realized',
                'Training Fee',
            ],
        }

        # Loop over the account data and create AccountHead and Account objects
        for head_type, accounts in account_data.items():
            # Create or get the AccountHead (grouping of accounts)
            head, created = AccountHead.objects.get_or_create(name=head_type, head_type=head_type.lower())
            if created:
                self.stdout.write(self.style.SUCCESS(f'Account Head "{head_type}" created successfully'))

            # Loop through the specific accounts under each AccountHead
            for account_name in accounts:
                # Create or get the Account, assigning it to the respective AccountHead
                account, created = Account.objects.get_or_create(name=account_name, account_type=head_type.lower(), account_head=head)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Account "{account_name}" created under "{head_type}" successfully'))

        self.stdout.write(self.style.SUCCESS('Default accounts and heads populated successfully.'))
