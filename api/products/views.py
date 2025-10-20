from django.db.models import Case, When
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.ecom.serializers import ProductDetailSerializer, ProductSearchSerializer
from apps.ecom.models import Product


class ProductVariantCombinationAPIView(APIView):
    def get(self, request, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)
            variants = product.variants.all()

            variant_data = []
            for variant in variants:
                # Prepare a list of attribute values for this variant
                attributes = variant.attributes.all()
                attribute_list = [{
                    'attribute_name': attribute.attribute.name,  # Get the attribute name
                    'value_name': attribute.value  # Get the attribute value
                } for attribute in attributes]

                variant_data.append({
                    'sku': variant.sku,
                    'price': variant.price,
                    'retail_price': variant.retail_price,
                    'stock_quantity': variant.stock_quantity,
                    'attributes': attribute_list
                })

            return Response({
                'product_name': product.name,
                'variants': variant_data
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


# typesense api 
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from apps.ecom.models import Product
import requests
from decouple import config, Csv

"""
http://127.0.0.1:8000/api/v1/product_search/?q=intell&query_by=name,description,category,attributes,tags&facet_by=attributes_flat&per_page=1&selected_filters[]=processor:intel_core_i5&selected_filters[]=generation:9th_gen

"""
from collections import defaultdict

@require_GET
def product_search_typesense_old(request):
    # Extract search parameters from the request
    query = request.GET.get('q', '*')
    query_by = request.GET.get('query_by', 'name,description,category,attributes,tags')
    facet_by = request.GET.get('facet_by', 'attributes_flat')
    category = request.GET.get('category', '')
    per_page = request.GET.get('per_page', '250')
    page = request.GET.get('page', 1)
    selected_filters = request.GET.getlist('selected_filters[]')  # Note the [] for multiple values

    api_key = config('TYPESENSE_KEY')
    api_ip = config('TYPESENSE_IP')
    api_port = config('TYPESENSE_PORT')

    # Build the Typesense search parameters
    params = {
        'q': query,
        'query_by': query_by,
        'facet_by': facet_by,
        'per_page': per_page,
        'page': page,
        'include_fields': 'id,name'
    }

    # Initialize filter expressions list
    filter_expressions = []

    # Add category filter if present
    if category:
        # Ensure proper syntax by wrapping the category value in quotes
        category_filter = f'{category}'
        filter_expressions.append(category_filter)

    # Add attribute filters
    if selected_filters:
        # Group filters by attribute names
        filters_by_attr = defaultdict(list)
        for f in selected_filters:
            if ':' in f:
                attr_name, attr_value = f.split(':', 1)
                filters_by_attr[attr_name].append(attr_value)

        # Build filter expressions
        for attr_name, values in filters_by_attr.items():
            # Combine multiple values for the same attribute with '||'
            attr_expressions = [f'attributes_flat:="{attr_name}:{value}"' for value in values]
            grouped_expr = '' + ' || '.join(attr_expressions) + ''
            filter_expressions.append(grouped_expr)

    # Combine all filters using '&&'
    if filter_expressions:
        params['filter_by'] = ' && '.join(filter_expressions)

    # Construct the Typesense search URL
    typesense_url = f'http://{api_ip}:{api_port}/collections/products/documents/search'
    headers = {'X-TYPESENSE-API-KEY': api_key}

    try:
        print("xxxxxxx",params)
        # Send the search request to Typesense
        response = requests.get(typesense_url, params=params, headers=headers)
        data = response.json()
    except Exception as e:
        return JsonResponse({'error': 'Error fetching search results from Typesense', 'details': str(e)}, status=500)

    # Extract product IDs from the Typesense search results
    hits = data.get('hits', [])
    product_ids = [hit['document']['id'] for hit in hits]

    # Fetch additional product details from the Django ORM
    products = Product.objects.filter(id__in=product_ids)
    # products_dict = {str(product.id): product for product in products}

    # # Enrich Typesense results with data from the Django ORM
    # combined_results = []
    # for hit in hits:
    #     doc = hit['document']
    #     product_id = doc['id']
    #     product = products_dict.get(product_id)
    #     if product:
    #         price = None  # Initialize price as None

    #         # Try to get price from default_variant
    #         if product.default_variant and product.default_variant.retail_price is not None:
    #             price = float(product.default_variant.retail_price)
    #         # Else try to get price from the first variant
    #         elif product.variants.exists():
    #             first_variant = product.variants.first()
    #             if first_variant.retail_price is not None:
    #                 price = float(first_variant.retail_price)

    #         # If price is still None, you can set a default value or handle it accordingly
    #         if price is None:
    #             price = 0.0  # Or handle as needed

    #         # Add additional fields from the Django model
    #         doc['price'] = price
    #         doc['stock'] = "ase"
    #         # Include other fields as necessary
    #     combined_results.append({
    #         'document': doc,
    #         'highlight': hit.get('highlight', {}),
    #         'highlights': hit.get('highlights', []),
    #     })

    # Replace the hits in the response data with the enriched results
    # data['hits'] = []
    data['products'] = ProductSearchSerializer(products,many=True).data

    return JsonResponse(data)



@require_GET
def product_search_typesense(request):
    # Extract search parameters from the request
    query = request.GET.get('q', '*')
    query_by = request.GET.get('query_by', 'name,description,category,attributes,tags')
    facet_by = request.GET.get('facet_by', 'attributes_flat')
    category = request.GET.get('category', '')
    per_page = request.GET.get('per_page', '250')
    page = request.GET.get('page', 1)
    selected_filters = request.GET.getlist('selected_filters[]')  # Note the [] for multiple values

    api_key = config('TYPESENSE_KEY')
    api_ip = config('TYPESENSE_IP')
    api_port = config('TYPESENSE_PORT')

    # Build the Typesense search parameters
    params = {
        'q': query,
        'query_by': query_by+',embedding',
        'facet_by': facet_by + ',tags',
        'per_page': per_page,
        'page': page,
        'include_fields': 'id,name'
    }

    # Initialize filter expressions list
    filter_expressions = []

    # Add category filter if present
    if category:
        # Ensure proper syntax by wrapping the category value in quotes
        category_filter = f'{category}'
        filter_expressions.append(category_filter)

    # Add attribute filters
    if selected_filters:
        # Group filters by attribute names
        filters_by_attr = defaultdict(list)
        for f in selected_filters:
            if ':' in f:
                attr_name, attr_value = f.split(':', 1)
                filters_by_attr[attr_name].append(attr_value)

        # Build filter expressions
        for attr_name, values in filters_by_attr.items():
            # Combine multiple values for the same attribute with '||'
            attr_expressions = [f'attributes_flat:="{attr_name}:{value}"' for value in values]
            grouped_expr = '' + ' || '.join(attr_expressions) + ''
            filter_expressions.append(grouped_expr)

    # Combine all filters using '&&'
    if filter_expressions:
        params['filter_by'] = ' && '.join(filter_expressions)

    # Construct the Typesense search URL
    typesense_url = f'http://{api_ip}:{api_port}/collections/products/documents/search'
    headers = {'X-TYPESENSE-API-KEY': api_key}


    

    try:
        print("xxxxxxx",params)
        # Send the search request to Typesense
        response = requests.get(typesense_url, params=params, headers=headers)
        data = response.json()
    except Exception as e:
        return JsonResponse({'error': 'Error fetching search results from Typesense', 'details': str(e)}, status=500)
    
    try:
        if query is not None:
            search_parameters_agreegator = {
                'q': query,
                'query_by': 'query',
                'per_page': 10,
                'page': 1

            }
            res = client.collections['product_queries'].documents.search(search_parameters_agreegator)
            q_values = [item["document"]["q"] for item in res['hits']]

         

            data['top_searches'] = q_values
    except Exception as e:
            print(e)
            pass

    # Extract product IDs from the Typesense search results
    hits = data.get('hits', [])
    product_ids = [hit['document']['id'] for hit in hits]

    # Fetch additional product details from the Django ORM
    products = Product.objects.filter(id__in=product_ids)
    # products_dict = {str(product.id): product for product in products}

    data['products'] = ProductSearchSerializer(products,many=True).data

    return JsonResponse(data)



#similar product api
from apps.helpers import client

class SimilarProductView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None, id=None):
        try:
            product_id = self.request.GET.get('product_id', '')
            
            # Construct search parameters for the embedding-based similarity search
            search_parameters = {
                'q': '*',
                'vector_query': f'embedding:([], id: {product_id})',
                'include_fields': 'id',
                'per_page': 12,
                'page': 1
            }

            # Query Typesense for similar products based on the embedding vector
            res = client.collections['products'].documents.search(search_parameters)  # Update 'product_collection' to your actual collection name
            similar_product_ids = [hit['document']['id'] for hit in res['hits']]

            # Preserve the ordering of similar products from Typesense
            preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(similar_product_ids)])

            # Query the database for Product instances matching the similar IDs and order them
            queryset = Product.objects.filter(id__in=similar_product_ids).order_by(preserved_order)
            
            # Serialize the resulting products
            serialized_products = ProductDetailSerializer(queryset, many=True, context={'request': request})

            return Response(serialized_products.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Not Found", "details": str(e)}, status=status.HTTP_403_FORBIDDEN)
        
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from apps.ecom.models import FavoriteProductVariant, ProductVariant
from django.shortcuts import get_object_or_404

class FavoriteProductVariantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteProductVariant.objects.filter(user=self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset()
        data = [{
            'id': fav.id,
            'product_variant': {
                'id': fav.product_variant.id,
                'sku': fav.product_variant.sku,
                'price': str(fav.product_variant.price),
                'image': fav.product_variant.image.url if fav.product_variant.image else None,
                'product_name': fav.product_variant.product.name,
            },
            'created_at': fav.created_at
        } for fav in queryset]
        return Response(data)

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        variant = get_object_or_404(ProductVariant, id=pk)
        favorite, created = FavoriteProductVariant.objects.get_or_create(
            user=request.user,
            product_variant=variant
        )
        if created:
            return Response({
                'message': 'Product variant added to favorites'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Product variant already in favorites'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_from_favorites(self, request, pk=None):
        variant = get_object_or_404(ProductVariant, id=pk)
        try:
            favorite = FavoriteProductVariant.objects.get(
                user=request.user,
                product_variant=variant
            )
            favorite.delete()
            return Response({
                'message': 'Product variant removed from favorites'
            }, status=status.HTTP_200_OK)
        except FavoriteProductVariant.DoesNotExist:
            return Response({
                'message': 'Product variant not in favorites'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def check_favorite(self, request, pk=None):
        variant = get_object_or_404(ProductVariant, id=pk)
        is_favorite = FavoriteProductVariant.objects.filter(
            user=request.user,
            product_variant=variant
        ).exists()
        return Response({
            'is_favorite': is_favorite
        })