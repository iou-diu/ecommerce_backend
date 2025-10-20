import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.ecom.management.commands.sample_products import sample_products
from apps.ecom.models import Product  # Adjust to match your models
from apps.helpers import client  # Assuming you have a client setup for Typesense

class Command(BaseCommand):
    help = 'Manage Typesense schema for products, with options to create schema, delete, or reindex data'

    def add_arguments(self, parser):
        parser.add_argument('command_name', type=str, help='Choose from schema, destroy, reindex, or sample')

    def handle(self, *args, **kwargs):
        command_name = kwargs['command_name']

        if client.operations.is_healthy():
            if command_name == 'schema':
                # Updated schema with attributes_flat
                schema = {
                    "name": "products",
                    "enable_nested_fields": True,
                    'symbols_to_index': ["-","&","+"],
                    "fields": [
                        {"name": "id", "type": "string", "facet": False},
                        {"name": "name", "type": "string", "facet": False},
                        {"name": "description", "type": "string", "facet": False},
                        {"name": "brand", "type": "string", "facet": True},
                        {"name": "category", "type": "string", "facet": True, "optional": True},
                        {"name": "price", "type": "float", "facet": True},
                        {"name": "tags", "type": "string[]", "facet": True, "optional": True},
                        {"name": "attributes", "type": "object[]", "facet": False, "optional": True},
                        {"name": "attributes_flat", "type": "string[]", "facet": True, "optional": True},
                        {
                            "name" : "embedding",
                            "type" : "float[]",
                            "embed": {
                                "from": [
                                    "name",
                                    "description",
                                    "category",
                                    "tags",
                                    "attributes_flat",
                                ],
                                "model_config": {
                                "model_name": "ts/all-MiniLM-L12-v2"
                                }
                            }
                        }
                        # Add other fields as needed
                    ],
                    "default_sorting_field": "price",
                }

                try:
                    res = client.collections.create(schema)
                    print("Schema created:", res)
                except Exception as e:
                    print("Error creating schema:", e)

            elif command_name == 'destroy':
                try:
                    res = client.collections['products'].delete()
                    print("Schema deleted:", res)
                except Exception as e:
                    print("Error deleting schema:", e)

            elif command_name == 'reindex':
                try:
                    products = Product.objects.all()

                    for product in products:
                        brand = product.brand.name if product.brand else "Unknown"
                        category = product.category.name if product.category else "Uncategorized"
                        tags = [tag.name for tag in product.tags.all()]
                        
                        # Prepare attributes list
                        attributes = []
                        attributes_flat = []
                        for product_attr in product.product_attributes.all():
                            attribute_name = product_attr.attribute.name.lower()
                            for attr_value in product_attr.values.all():
                                value = attr_value.value.lower().replace(" ", "_")
                                attributes.append({"name": attribute_name, "value": value})
                                attributes_flat.append(f"{attribute_name}:{value}")

                        # Construct the document for Typesense
                        document = {
                            "id": str(product.id),
                            "name": product.name,
                            "description": product.description or "",
                            "brand": brand,
                            "category": category,
                            "price": float(0),
                            "tags": tags,
                            "attributes": attributes,
                            "attributes_flat": attributes_flat,
                            # Include other fields as needed
                        }


                        print(document)

                        # Index the document in Typesense
                        res = client.collections['products'].documents.upsert(document)
                        print("Indexed product ID:", product.id)

                except Exception as e:
                    print("Error reindexing products:", e)

            elif command_name == 'sample':
                # Upsert sample products to Typesense
                for product in sample_products[:5]:
                    try:
                        # Ensure attributes_flat is created for sample products
                        attributes_flat = [f"{attr['name']}:{attr['value']}" for attr in product.get('attributes', [])]
                        product['attributes_flat'] = attributes_flat

                        print(product)

                        res = client.collections['products'].documents.upsert(product)
                        print("Upserted sample product:", product["name"])
                    except Exception as e:
                        print(f"Error upserting product {product['name']}:", e)

            else:
                print("Unknown command")
        else:
            print("Typesense is disconnected or an error occurred")
