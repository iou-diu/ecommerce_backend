from django.core.management.base import BaseCommand
import re
from apps.ecom.models import Product  # Update this import to match your actual Product model path
from apps.helpers import client  # Ensure client is correctly configured for your Typesense instance



class Command(BaseCommand):
    help = 'Manage Typesense schema for popular queries in eCommerce'

    def add_arguments(self, parser):
        parser.add_argument('command_name', type=str,
                            help='Run: python manage.py typesense_ecommerce schema, reindex, rules, or search')

    def handle(self, *args, **kwargs):
        command_name = kwargs['command_name']

        if client.operations.is_healthy():
            if command_name == 'schema':
                # Define schema for popular eCommerce queries
                schema = {
                    'name': 'product_queries',
                    'fields': [
                        {
                            'name': 'query',
                            'type': 'string'
                        },
                        {
                            'name': 'count',
                            'type': 'int32'
                        }
                    ],
                    'default_sorting_field': 'count'
                }
                
                try:
                    # Create the collection for tracking popular queries
                    res = client.collections.create(schema)
                    print("Schema created:", res)
                except Exception as e:
                    print("Schema creation failed:", e)

            elif command_name == 'rules':
                try:
                    # Set up popular query aggregation rules for the eCommerce collection
                    create_response = client.analytics.rules.create({
                        "name": "popular_product_queries",
                        "type": "popular_queries",
                        "params": {
                            "source": {
                                "collections": ["products"]  
                            },
                            "destination": {
                                "collection": "product_queries"
                            },
                            "limit": 1000
                        }
                    })
                    print("Rules created:", create_response)
                except Exception as e:
                    print("Rules creation failed:", e)

            elif command_name == 'search':
                try:
                    # Example of a multi-collection search query
                    query = "processor"  # Example search term, could be dynamically set
                    search_requests = {
                        'searches': [
                            {
                                'collection': 'product_queries',
                                'q': query,
                                'query_by': 'query'
                            },
                            {
                                'collection': 'products', 
                                'q': query,
                                'query_by': 'name,description,category,attributes,tags',  # Adjust fields as necessary
                                'include_fields': 'name,id',
                                'per_page': 5
                            }
                        ]
                    }

                    common_search_params = {}
                    x = client.multi_search.perform(search_requests, common_search_params)
                    print("Search results:", x)
                except Exception as e:
                    print("Search failed:", e)

            elif command_name == 'delete':
                try:
                    client.collections['product_queries'].documents['document_id'].delete()  # Replace 'document_id' as needed
                    print("Document deleted")
                except Exception as e:
                    print("Delete operation failed:", e)

        else:
            print("Typesense is disconnected or encountered an error.")
