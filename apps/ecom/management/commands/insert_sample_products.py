from django.core.management.base import BaseCommand
# from apps.ecom.management.commands.sample_products import sample_products
from apps.ecom.management.commands.sample_prod3 import sample_products

from apps.ecom.models import Product, Brand, Category, Tag, Attribute, AttributeValue, ProductAttribute
from django.utils.text import slugify
from django.db import transaction, IntegrityError
import random
import string
import logging
import sys
import uuid

class Command(BaseCommand):
    help = 'Creates new products in the database (skips existing ones)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable detailed debug logging',
        )

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.DEBUG if options['debug'] else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('product_import.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.create_products()

    def create_products(self):
        total_created = 0
        total_skipped = 0
        total_failed = 0
        error_details = []

        for index, product_data in enumerate(sample_products, start=1):
            try:
                with transaction.atomic():
                    product_name = product_data.get('name')
                    self.logger.info(f"Processing product {index}/{len(sample_products)}: {product_name}")
                    
                    # Skip if product already exists
                    if Product.objects.filter(name=product_name).exists():
                        self.logger.info(f"Skipping existing product: {product_name}")
                        total_skipped += 1
                        continue

                    # Validate required fields
                    required_fields = ['name', 'brand', 'category']
                    missing_fields = [field for field in required_fields if not product_data.get(field)]
                    if missing_fields:
                        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

                    # Handle Brand
                    brand_name = product_data.get('brand', '').strip()
                    if not brand_name:
                        raise ValueError("Brand name cannot be empty")
                    
                    brand_slug = self.get_unique_slug(Brand, brand_name)
                    brand, _ = Brand.objects.get_or_create(
                        name=brand_name,
                        defaults={'slug': brand_slug}
                    )

                    # Handle Category and Subcategory
                    category_name = product_data.get('category', '').strip()
                    subcategory_name = product_data.get('subcategory', '').strip() if 'subcategory' in product_data else None

                    if not category_name:
                        raise ValueError("Category name cannot be empty")

                    # Enforce uniqueness on Category names
                    category, created = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'slug': self.get_unique_slug(Category, category_name)}
                    )
                    if not created:
                        # Ensure the slug is correct if category already exists
                        if not category.slug:
                            category.slug = self.get_unique_slug(Category, category_name)
                            category.save()

                    if subcategory_name:
                        subcategory, created = Category.objects.get_or_create(
                            name=subcategory_name,
                            parent=category,
                            defaults={'slug': self.get_unique_slug(Category, subcategory_name)}
                        )
                        if not created:
                            # Ensure the slug is correct if subcategory already exists
                            if not subcategory.slug:
                                subcategory.slug = self.get_unique_slug(Category, subcategory_name)
                                subcategory.save()
                        product_category = subcategory
                    else:
                        product_category = category

                    # Create Product
                    short_uuid = uuid.uuid4().hex[:8]  # Get the first 8 characters

                    max_name_length = 50 - len(short_uuid) - 1  # Subtract length of UUID and hyphen
                    truncated_name = product_name[:max_name_length]
                    product = Product.objects.create(
                        name=f"{truncated_name}-{short_uuid}",
                        description=product_data.get('description', ''),
                        brand=brand,
                        category=product_category,
                    )

                    # Handle Tags
                    if 'tags' in product_data:
                        for tag_name in product_data['tags']:
                            if tag_name.strip():
                                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                                product.tags.add(tag)

                    # Handle Attributes
                    if 'attributes' in product_data:
                        for attr_data in product_data['attributes']:
                            if not all(key in attr_data for key in ['name', 'value']):
                                self.logger.warning(f"Skipping invalid attribute for product {product.name}: {attr_data}")
                                continue

                            attribute, _ = Attribute.objects.get_or_create(name=attr_data['name'])
                            attr_value_obj, _ = AttributeValue.objects.get_or_create(
                                attribute=attribute,
                                value=attr_data['value']
                            )
                            product_attribute, _ = ProductAttribute.objects.get_or_create(
                                product=product,
                                attribute=attribute
                            )
                            product_attribute.values.add(attr_value_obj)

                    total_created += 1
                    self.logger.info(f"Successfully created product: {product.name}")

            except IntegrityError as ie:
                total_failed += 1
                error_message = f"IntegrityError for product {product_data.get('name', 'Unknown')}: {str(ie)}"
                self.logger.error(error_message)
                error_details.append({
                    'product': product_data.get('name', 'Unknown'),
                    'error': str(ie),
                    'data': product_data
                })
            except Exception as e:
                total_failed += 1
                error_message = f"Failed to create product {product_data.get('name', 'Unknown')}: {str(e)}"
                self.logger.error(error_message)
                error_details.append({
                    'product': product_data.get('name', 'Unknown'),
                    'error': str(e),
                    'data': product_data
                })

        # Log summary
        self.logger.info(f"\nImport Summary:")
        self.logger.info(f"Total products processed: {len(sample_products)}")
        self.logger.info(f"Successfully created: {total_created}")
        self.logger.info(f"Skipped (already exist): {total_skipped}")
        self.logger.info(f"Failed: {total_failed}")

        # Log detailed errors if any
        if error_details:
            self.logger.error("\nDetailed Error Report:")
            for error in error_details:
                self.logger.error(f"\nProduct: {error['product']}")
                self.logger.error(f"Error: {error['error']}")
                self.logger.error(f"Data: {error['data']}")

    def get_unique_slug(self, model, name):
        """
        Generate a unique slug for the given model based on the name.
        """
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while model.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
