import json
import os
from django.core.management.base import BaseCommand
from apps.accounting.models import AccountHead, ExpenseCategory

class Command(BaseCommand):
    help = "Seed initial accounting data (AccountHeads and ExpenseCategories)"

    def handle(self, *args, **kwargs):
        # Correct path for management command to find the fixture
        # Build path relative to the app's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fixture_path = os.path.join(current_dir, '..', '..', 'fixtures', 'initial_accounting_data.json')
        fixture_path = os.path.normpath(fixture_path)

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f"Fixture file not found at {fixture_path}"))
            return

        with open(fixture_path, 'r') as file:
            data = json.load(file)

        # 1. Seed Account Heads
        self.stdout.write("Seeding Account Heads...")
        for head in data.get('account_heads', []):
            obj, created = AccountHead.objects.get_or_create(
                name=head['name'],
                head_type=head['head_type']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created AccountHead: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"AccountHead '{obj.name}' already exists."))

        # 2. Seed Expense Categories
        self.stdout.write("\nSeeding Expense Categories...")
        for cat in data.get('expense_categories', []):
            parent_obj, created = ExpenseCategory.objects.get_or_create(
                name=cat['name'],
                parent_category=None
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Parent Category: {parent_obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Parent Category '{parent_obj.name}' already exists."))
            
            # Handle subcategories
            for sub_name in cat.get('subcategories', []):
                sub_obj, sub_created = ExpenseCategory.objects.get_or_create(
                    name=sub_name,
                    parent_category=parent_obj
                )
                if sub_created:
                    self.stdout.write(self.style.SUCCESS(f"  - Created Subcategory: {sub_obj.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"  - Subcategory '{sub_obj.name}' already exists."))

        self.stdout.write(self.style.SUCCESS("\nSuccessfully seeded all global accounting data!"))
