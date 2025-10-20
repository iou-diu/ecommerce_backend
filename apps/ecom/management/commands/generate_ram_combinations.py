import itertools
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate and print all possible combinations of dynamic attribute options'

    def handle(self, *args, **kwargs):
        # Define the possible values for RAM, Color, and other attributes
        ram_options = ['4GB', '8GB', '16GB', '32GB', '64GB']
        color_options = ['Black', 'Silver', 'Grey', 'Blue', 'White', 'Red', 'Gold']
        storage_options = ['128GB SSD', '256GB SSD', '512GB SSD', '1TB HDD', '1TB SSD']
        
        # Dynamic input for any number of lists
        attribute_lists = [ram_options, color_options, storage_options]

        # Generate all possible combinations of the given attribute lists
        combinations = list(itertools.product(*attribute_lists))

        # Print the number of combinations
        print(f'Total combinations generated: {len(combinations)}')

        # Optionally, print out each combination
        # self.stdout.write(self.style.SUCCESS('Generated combinations:'))
        # for combination in combinations:
        #     self.stdout.write(f'{combination}')

        self.stdout.write(self.style.SUCCESS(f'Finished generating {len(combinations)} combinations.'))
