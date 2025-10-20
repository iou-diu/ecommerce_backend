import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.ecom.models import Category


class Command(BaseCommand):
    help = 'Populate database with computer-related categories and subcategories'

    categories_data = [
        ('Desktop Components', [
            'Processor',
            'Memory',
            'Storage Devices',
            'Graphics Cards',
            'Motherboards',
            'Cooling Systems',
            'Power Supplies',
            'Cases',
            'Optical Drives',
            'Sound Cards',
            'Network Cards',
            'USB Hubs',
            'Card Readers'
        ]),
        ('Office Supplies', [
            ('Printers', [
                'Laser Printers',
                'Inkjet Printers',
                'Dot Matrix Printers',
                'Photo Printers',
                'Multifunction Printers'
            ]),
            'Scanners',
            'Shredders',
            'Laminators',
            'Projectors',
            'Office Chairs',
            'Desk Accessories',
            'Binders',
            'Paper Trays',
            'Staplers',
            'Pens and Pencils',
            'Calendars',
            'Sticky Notes'
        ]),
        ('Laptops & Accessories', [
            'Laptop Stands',
            'Cooling Pads',
            'Laptop Bags',
            'Chargers',
            'Laptop Skins',
            'Screen Protectors',
            'Docking Stations',
            'External Keyboards',
            'External Mice',
            'Privacy Screens',
            'Webcams',
            'Portable Power Banks',
            'Laptop Locks'
        ]),
        ('Software', [
            'Operating Systems',
            'Productivity Software',
            'Antivirus',
            'Development Tools',
            'Database Management',
            'Graphics Software',
            'Video Editing Software',
            'Audio Editing Software',
            'CAD Software',
            'Office Suites',
            'Web Browsers',
            'Communication Software',
            'Security Software'
        ]),
        ('Networking Equipment', [
            'Routers',
            'Modems',
            'Switches',
            'Access Points',
            'Firewalls',
            'Network Cables',
            'Powerline Adapters',
            'Network Antennas',
            'Network Interface Cards',
            'Patch Panels',
            'Network Extenders',
            'Mesh Wi-Fi Systems',
            'Network Storage Devices'
        ]),
        ('Computer Peripherals', [
            'Monitors',
            'Keyboards',
            'Mice',
            'Headsets',
            'Speakers',
            'Microphones',
            'Webcams',
            'Graphic Tablets',
            'Gaming Controllers',
            'Joysticks',
            'Foot Pedals',
            'Trackballs',
            'Bluetooth Adapters'
        ]),
        ('Gaming Equipment', [
            'Gaming Laptops',
            'Gaming Desktops',
            'Gaming Monitors',
            'Gaming Keyboards',
            'Gaming Mice',
            'Gaming Headsets',
            'VR Headsets',
            'Game Consoles',
            'Console Controllers',
            'Game Capture Cards',
            'Racing Wheels',
            'Arcade Sticks',
            'Gaming Chairs'
        ]),
        ('Storage Devices', [
            'External Hard Drives',
            'Internal Hard Drives',
            'Solid State Drives',
            'Flash Drives',
            'Memory Cards',
            'NAS Devices',
            'RAID Arrays',
            'Optical Discs',
            'Tape Drives',
            'Portable SSDs',
            'Cloud Storage',
            'Network Drives',
            'Storage Accessories'
        ]),
        ('Smart Home Devices', [
            'Smart Speakers',
            'Smart Displays',
            'Smart Plugs',
            'Smart Lights',
            'Smart Thermostats',
            'Smart Locks',
            'Smart Cameras',
            'Smart Doorbells',
            'Smart Sensors',
            'Smart Hubs',
            'Robot Vacuums',
            'Smart Blinds',
            'Smart Irrigation Controllers'
        ]),
        ('Mobile Accessories', [
            'Phone Cases',
            'Screen Protectors',
            'Charging Cables',
            'Power Banks',
            'Car Mounts',
            'Wireless Chargers',
            'Bluetooth Earbuds',
            'Selfie Sticks',
            'Stylus Pens',
            'Portable Speakers',
            'Headphone Adapters',
            'Camera Lenses for Phones',
            'Memory Cards for Phones'
        ]),
        ('Audio Equipment', [
            'Headphones',
            'Earbuds',
            'Speakers',
            'Home Theater Systems',
            'Soundbars',
            'Amplifiers',
            'Receivers',
            'Microphones',
            'Turntables',
            'Mixers',
            'Audio Cables',
            'Digital Audio Players',
            'DACs (Digital-to-Analog Converters)'
        ]),
        ('Camera Equipment', [
            'DSLR Cameras',
            'Mirrorless Cameras',
            'Compact Cameras',
            'Camera Lenses',
            'Tripods',
            'Camera Bags',
            'Camera Straps',
            'Memory Cards for Cameras',
            'Lens Filters',
            'Flashes',
            'Lighting Equipment',
            'Action Cameras',
            'Camera Drones'
        ]),
        ('Office Furniture', [
            'Desks',
            'Chairs',
            'File Cabinets',
            'Bookshelves',
            'Cubicles',
            'Office Partitions',
            'Reception Desks',
            'Conference Tables',
            'Desk Lamps',
            'Standing Desks',
            'Ergonomic Accessories',
            'Whiteboards',
            'Office Plants'
        ]),
        ('Computer Accessories', [
            'Cooling Pads',
            'USB Hubs',
            'Keyboard Covers',
            'Mouse Pads',
            'Wrist Rests',
            'Cable Management',
            'Dust Covers',
            'Monitor Stands',
            'Laptop Locks',
            'Laptop Stands',
            'Headphone Stands',
            'VR Accessories',
            'Screen Cleaners'
        ]),
        ('Wearable Technology', [
            'Smartwatches',
            'Fitness Trackers',
            'VR Headsets',
            'AR Glasses',
            'Smart Rings',
            'Smart Clothing',
            'Health Monitors',
            'Wearable Cameras',
            'GPS Trackers',
            'Sleep Monitors',
            'Heart Rate Monitors',
            'Hearing Aids',
            'Wearable Battery Packs'
        ]),
        ('Computer Cleaning Supplies', [
            'Screen Cleaners',
            'Compressed Air',
            'Keyboard Cleaners',
            'Microfiber Cloths',
            'Anti-Static Brushes',
            'Cleaning Swabs',
            'Lens Cleaners',
            'Sanitizing Wipes',
            'Cleaning Sprays',
            'Vacuum Cleaners',
            'Cleaning Kits',
            'Cable Ties',
            'Dust Covers'
        ]),
        ('Power Protection', [
            'UPS (Uninterruptible Power Supply)',
            'Surge Protectors',
            'Power Strips',
            'Voltage Regulators',
            'Battery Backup Systems',
            'Power Conditioners',
            'Portable Generators',
            'Extension Cords',
            'Battery Chargers',
            'Rechargeable Batteries',
            'Inverters',
            'Circuit Breakers',
            'Power Cables'
        ]),
        ('3D Printing Equipment', [
            '3D Printers',
            '3D Printer Filaments',
            '3D Scanners',
            'Resin Printers',
            'Print Beds',
            'Nozzles',
            'Extruders',
            'Build Plates',
            'Filament Dryers',
            'Enclosures',
            'Slicers',
            'Calibration Tools',
            '3D Printing Software'
        ]),
        ('Computer Security Equipment', [
            'Encryption Software',
            'Anti-Virus Software',
            'Firewall Software',
            'Password Managers',
            'Security Cameras',
            'Fingerprint Scanners',
            'Smart Locks',
            'Biometric Devices',
            'RFID Scanners',
            'Security Tokens',
            'Smart Cards',
            'Security Gateways',
            'Access Control Systems'
        ])
    ]


    def handle(self, *args, **kwargs):
        self.populate_categories(self.categories_data)
        self.stdout.write(self.style.SUCCESS('Successfully populated categories and subcategories.'))

    def get_unique_slug(self, name):
        slug = slugify(name)
        unique_slug = slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug
    
    def populate_categories(self, categories, parent=None):
        for item in categories:
            if isinstance(item, tuple):
                category_name, subcategories = item
            else:
                category_name = item
                subcategories = []

            # Generate a unique slug
            unique_slug = self.get_unique_slug(category_name)

            # Create or update the main category
            category, created = Category.objects.update_or_create(
                name=category_name,
                parent=parent,
                defaults={
                    'slug': unique_slug,
                    'description': f'Description for {category_name}',
                    'meta_title': f'Meta title for {category_name}',
                    'meta_description': f'Meta description for {category_name}',
                    'is_active': True,
                }
            )

            # Recursive call for subcategories
            if subcategories:
                self.populate_categories(subcategories, parent=category)