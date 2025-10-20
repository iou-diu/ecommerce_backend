from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

from django.views.generic import TemplateView
from rest_framework import viewsets

from .models import Hotspot, HotspotItem
from ..ecom.models import Product


@csrf_exempt  # Disable CSRF for testing purposes; use proper CSRF handling in production
def create_hotspot_api(request):
    if request.method == 'POST':
        try:
            # Retrieve the title and image from the form
            title = request.POST.get('title')
            image = request.FILES.get('image')
            hotspot_items_data = json.loads(request.POST.get('hotspot_items', '[]'))

            # Check if title and image are provided
            if not title or not image:
                return JsonResponse({'error': 'Title and image are required fields.'}, status=400)

            # Create the Hotspot object
            hotspot = Hotspot.objects.create(title=title, image=image)

            # Create associated HotspotItem objects
            for item in hotspot_items_data:
                HotspotItem.objects.create(
                    hot_spot=hotspot,
                    product_id=item['product_id'],
                    x_coordinate=item['x'],
                    y_coordinate=item['y']
                )

            return JsonResponse({'message': 'Hotspot created successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in hotspot_items.'}, status=400)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_products(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({'error': 'Search query is required'}, status=400)

    products = Product.objects.filter(name__icontains=query).values('id', 'name')

    return JsonResponse({
        'products': list(products),
        'total_results': len(products)
    })


class HotspotAddView(TemplateView):
    template_name = 'hotspot.html'
