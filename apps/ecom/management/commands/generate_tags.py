from django.core.management.base import BaseCommand
from apps.ecom.models import Tag  # Adjust the import based on your app structure

class Command(BaseCommand):
    help = 'Populate the database with common eCommerce tags related to furniture products'

    def handle(self, *args, **kwargs):
        # List of tags
        tags_list = [
            # Living Room
            'sofa', 'couch', 'recliner', 'coffee table', 'tv stand', 'armchair', 'ottoman', 'bookshelf', 
            'side table', 'futon', 'loveseat', 'sectional sofa', 'chesterfield sofa', 'accent chair',
            
            # Bedroom
            'bed frame', 'mattress', 'nightstand', 'dresser', 'wardrobe', 'chest of drawers', 'vanity table', 
            'headboard', 'bunk bed', 'king size bed', 'queen size bed', 'single bed', 'canopy bed',
            
            # Dining Room
            'dining table', 'dining chairs', 'sideboard', 'buffet', 'bar stools', 'china cabinet', 
            'kitchen island', 'dining set', 'pub table', 'bench',
            
            # Office
            'office desk', 'office chair', 'filing cabinet', 'desk organizer', 'conference table', 
            'ergonomic chair', 'standing desk', 'computer desk', 'executive chair', 'bookcase',
            
            # Outdoor / Patio
            'patio set', 'garden bench', 'sun lounger', 'outdoor dining table', 'hammock', 'deck chairs', 
            'gazebo', 'adirondack chair', 'outdoor sofa', 'bistro set',
            
            # Storage & Hallway
            'shoe rack', 'coat rack', 'wall shelves', 'storage bench', 'trunk', 'closet organizer', 
            'entryway table', 'console table',
            
            # Styles & Themes
            'modern furniture', 'vintage', 'rustic', 'minimalist', 'luxury', 'industrial', 
            'mid-century modern', 'scandinavian', 'bohemian', 'contemporary',
            
            # Materials
            'solid wood', 'oak', 'teak', 'walnut', 'leather', 'fabric', 'velvet', 'rattan', 
            'metal', 'glass', 'mahogany', 'pine', 'engineered wood',
            
            # Kid's Furniture
            'kids bed', 'study table', 'toy box', 'nursery chair', 'crib', 'changing table', 
            'play table', 'kids bookshelf',
            
            # Decor & Accents
            'mirror', 'wall art', 'rug', 'curtains', 'cushion', 'floor lamp', 'chandelier', 
            'pendant light', 'divider', 'screen'
        ]


        # Create the tags if they don't already exist
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Tag '{tag_name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Tag '{tag_name}' already exists"))
