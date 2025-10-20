from django.core.management.base import BaseCommand
from apps.ecom.models import Attribute, AttributeValue

class Command(BaseCommand):
    help = 'Populate the most common attributes and their associated values'

    def handle(self, *args, **kwargs):
        attributes_and_values = {
            # Electronics Attributes
            'Processor': ['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core i9', 'AMD Ryzen 3', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9'],
            'Generation': ['8th Gen', '9th Gen', '10th Gen', '11th Gen', '12th Gen', '13th Gen', 'AMD Zen 2', 'AMD Zen 3'],
            'RAM': ['4GB', '8GB', '16GB', '32GB', '64GB'],
            'Storage': ['128GB SSD', '256GB SSD', '512GB SSD', '1TB HDD', '1TB SSD', '2TB HDD'],
            'Graphics Card': ['NVIDIA GTX 1050', 'NVIDIA GTX 1650', 'NVIDIA RTX 2060', 'NVIDIA RTX 3060', 'AMD Radeon RX 580', 'AMD Radeon RX 5700'],
            'Display': ['14-inch', '15.6-inch', '17-inch', 'Full HD', '4K UHD', 'Touchscreen'],
            'Battery': ['3-cell', '4-cell', '6-cell'],
            'Weight': ['1kg', '1.5kg', '2kg', '2.5kg', '3kg'],
            'Operating System': ['Windows 10', 'Windows 11', 'Ubuntu', 'Free DOS', 'Mac OS'],
            'Color': ['Black', 'Silver', 'Grey', 'Blue', 'White', 'Red', 'Gold'],
            'Screen Resolution': ['1920x1080', '2560x1440', '3840x2160', '4K UHD', '5K UHD'],
            'Connectivity': ['Wi-Fi 5', 'Wi-Fi 6', 'Bluetooth 4.2', 'Bluetooth 5.0', 'Ethernet', 'USB Type-C', 'HDMI', 'Thunderbolt'],
            'Storage Type': ['HDD', 'SSD', 'NVMe SSD'],
            'Refresh Rate': ['60Hz', '75Hz', '120Hz', '144Hz', '240Hz'],

            # Clothing Attributes
            'T-Shirt Size': ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL'],
            'T-Shirt Material': ['Cotton', 'Polyester', 'Cotton Blend', 'Wool', 'Linen'],
            'T-Shirt Fit': ['Slim Fit', 'Regular Fit', 'Loose Fit'],
            'T-Shirt Sleeve Length': ['Short Sleeve', 'Long Sleeve', 'Sleeveless'],
            'Shoe Size': ['6', '7', '8', '9', '10', '11', '12', '13', '14'],
            'Shoe Type': ['Sneakers', 'Formal', 'Boots', 'Sandals', 'Slippers'],
            'Shoe Color': ['Black', 'White', 'Brown', 'Blue', 'Red', 'Green'],
            'Clothing Gender': ['Men', 'Women', 'Unisex'],
            
            # More Electronics Attributes
            'Laptop Type': ['Gaming Laptop', 'Business Laptop', '2-in-1 Convertible', 'Ultrabook'],
            'Camera': ['720p HD Webcam', '1080p HD Webcam', 'No Camera'],
            'Keyboard Backlight': ['Yes', 'No'],
            'Charger Type': ['USB-C', 'Standard AC Adapter', 'MagSafe'],
            
            # Home Appliance Attributes
            'Washing Machine Capacity': ['6kg', '7kg', '8kg', '10kg', '12kg'],
            'Refrigerator Type': ['Single Door', 'Double Door', 'Side-by-Side', 'French Door'],
            'Air Conditioner Capacity': ['1 Ton', '1.5 Ton', '2 Ton'],
            'Oven Capacity': ['20L', '25L', '30L', '40L'],
        }



        for attribute_name, values in attributes_and_values.items():
            # Create or get the Attribute
            attribute, created = Attribute.objects.get_or_create(name=attribute_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Attribute "{attribute_name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Attribute "{attribute_name}" already exists'))

            # Create associated AttributeValues
            for value in values:
                attribute_value, value_created = AttributeValue.objects.get_or_create(attribute=attribute, value=value)
                if value_created:
                    self.stdout.write(self.style.SUCCESS(f'  - Value "{value}" for attribute "{attribute_name}" created'))
                else:
                    self.stdout.write(self.style.WARNING(f'  - Value "{value}" for attribute "{attribute_name}" already exists'))

        self.stdout.write(self.style.SUCCESS('Finished populating common attributes and values.'))