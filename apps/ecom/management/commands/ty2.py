import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.ecom.models import Product, ProductVariant, Brand, Category, Tag  # Adjust to match your models
from apps.helpers import client  # Assuming you have a client setup for Typesense

class Command(BaseCommand):
    help = 'Manage Typesense schema for products, with options to create schema, delete, or reindex data'

    def add_arguments(self, parser):
        parser.add_argument('command_name', type=str, help='Choose from schema, destroy, or reindex')

    def handle(self, *args, **kwargs):
        command_name = kwargs['command_name']

        if client.operations.is_healthy():
            if command_name == 'schema':
                schema = {
                    "name": "products",
                    "enable_nested_fields": True,
                    "fields": [
                        {"name": "id", "type": "string", "facet": False},
                        {"name": "name", "type": "string", "facet": False},
                        {"name": "description", "type": "string", "facet": False},
                        {"name": "brand", "type": "string", "facet": True},
                        {"name": "category", "type": "string", "facet": True,"optional": True},
                        {"name": "price", "type": "float", "facet": True},
                        {"name": "tags", "type": "string[]", "facet": True,"optional": True},
                        {"name": "attributes", "type": "string[]", "facet": True,"optional": True},
                      
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
                        attributes = [attr.name for attr in product.product_attributes.all()]

           

                        document = {
                            "id": str(product.id),
                            "name": product.name,
                            "description": product.description or "",
                            "brand": brand,
                            "category": category,
                            "price": float(product.price),
                            "discount_type": product.discount_type,
                            "discount_amount": float(product.discount_amount or 0.0),
                            "discount_end_date": int(product.discount_end_date.timestamp()) if product.discount_end_date else 0,
                            "is_active": product.is_active,
                            "tags": tags,
                            "attributes": attributes,
                            "rating": float(product.rating or 0.0),
                            "stock_quantity": product.stock_quantity,
                            "warranty": product.warranty or "",
                            "sku": product.sku,
                        }

                        res = client.collections['products'].documents.upsert(document)
                        print("Indexed product ID:", product.id)
                except Exception as e:
                    print("Error reindexing products:", e)
            elif command_name == 'sample':
                sample_products = [
                    {
                        "id": "1",
                        "name": "Intel Core i9 Processor",
                        "description": "High-performance Intel processor with 8 cores",
                        "brand": "Intel",
                        "category": "Processor",
                        "price": 500.00,
                        "tags": ["processor", "high-performance", "gaming"],
                        "attributes": ["8 cores", "3.5 GHz", "10th Gen"]
                    },
                    {
                        "id": "2",
                        "name": "AMD Ryzen 7 Processor",
                        "description": "Powerful AMD processor for multitasking",
                        "brand": "AMD",
                        "category": "Processor",
                        "price": 450.00,
                        "tags": ["processor", "multitasking", "high-performance"],
                        "attributes": ["8 cores", "3.8 GHz", "3rd Gen"]
                    },
                    {
                        "id": "3",
                        "name": "Intel Core i5 Processor",
                        "description": "Mid-range Intel processor for general use",
                        "brand": "Intel",
                        "category": "Processor",
                        "price": 250.00,
                        "tags": ["processor", "general-use", "mid-range"],
                        "attributes": ["6 cores", "2.9 GHz", "10th Gen"]
                    },
                    {
                        "id": "4",
                        "name": "AMD Ryzen 5 Processor",
                        "description": "Efficient AMD processor for budget builds",
                        "brand": "AMD",
                        "category": "Processor",
                        "price": 200.00,
                        "tags": ["processor", "budget", "efficient"],
                        "attributes": ["6 cores", "3.2 GHz", "3rd Gen"]
                    },
                    {
                        "id": "5",
                        "name": "Intel Core i3 Processor",
                        "description": "Affordable Intel processor for entry-level use",
                        "brand": "Intel",
                        "category": "Processor",
                        "price": 120.00,
                        "tags": ["processor", "entry-level", "affordable"],
                        "attributes": ["4 cores", "2.5 GHz", "10th Gen"]
                    },
                    {
                        "id": "6",
                        "name": "Dell 24-inch Monitor",
                        "description": "Full HD monitor with 75Hz refresh rate",
                        "brand": "Dell",
                        "category": "Monitor",
                        "price": 150.00,
                        "tags": ["monitor", "FHD", "75Hz"],
                        "attributes": ["1920x1080", "75Hz", "IPS"]
                    },
                    {
                        "id": "7",
                        "name": "Samsung 27-inch Monitor",
                        "description": "QHD monitor with 144Hz refresh rate",
                        "brand": "Samsung",
                        "category": "Monitor",
                        "price": 350.00,
                        "tags": ["monitor", "QHD", "144Hz"],
                        "attributes": ["2560x1440", "144Hz", "VA"]
                    },
                    {
                        "id": "8",
                        "name": "LG 32-inch UltraWide Monitor",
                        "description": "UltraWide monitor with 60Hz refresh rate",
                        "brand": "LG",
                        "category": "Monitor",
                        "price": 400.00,
                        "tags": ["monitor", "UltraWide", "60Hz"],
                        "attributes": ["2560x1080", "60Hz", "IPS"]
                    },
                    {
                        "id": "9",
                        "name": "Acer Predator 27-inch Monitor",
                        "description": "Gaming monitor with G-Sync and 144Hz refresh rate",
                        "brand": "Acer",
                        "category": "Monitor",
                        "price": 450.00,
                        "tags": ["monitor", "gaming", "G-Sync"],
                        "attributes": ["2560x1440", "144Hz", "IPS"]
                    },
                    {
                        "id": "10",
                        "name": "BenQ 24-inch Monitor",
                        "description": "Budget-friendly monitor with FHD resolution",
                        "brand": "BenQ",
                        "category": "Monitor",
                        "price": 130.00,
                        "tags": ["monitor", "budget", "FHD"],
                        "attributes": ["1920x1080", "60Hz", "TN"]
                    }
                ]

                # Upsert sample products to Typesense
                for product in sample_products:
                    try:
                        res = client.collections['products'].documents.upsert(product)
                        print("Upserted sample product:", product["name"])
                    except Exception as e:
                        print(f"Error upserting product {product['name']}:", e)


            else:
                print("Unknown command")
        else:
            print("Typesense is disconnected or an error occurred")


import requests

url = "localhost:8108/collections/products/documents/search?q=*&query_by=name,description,category&facet_by=tags,attributes.value&filter_by=attributes.value:=6"

payload = {}
headers = {
  'x-typesense-api-key': '',
  'Cookie': 'csrftoken=BdOgYaOk6onAI1o8mVZLgLUiAJuPzI2J'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


import requests

url = "localhost:8108/collections/products/documents/search?q=*&query_by=name,description,category&facet_by=tags,attributes.value&filter_by=category:=Headset"

payload = {}
headers = {
  'x-typesense-api-key': '',
  'Cookie': 'csrftoken=BdOgYaOk6onAI1o8mVZLgLUiAJuPzI2J'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
