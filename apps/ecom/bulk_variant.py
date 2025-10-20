# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json
from apps.ecom.models import Product, ProductVariant, ProductAttribute, AttributeValue


class ProductVariantBulkView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'bulk_add.html'
    permission_required = 'ecom.change_productvariant'

    def post(self, request, pk):
        try:
            product = get_object_or_404(Product, pk=pk)
            variants_data = json.loads(request.POST.get('variants', '[]'))

            created_variants = []

            for index, variant_data in enumerate(variants_data):
                # Create ProductVariant instance
                variant = ProductVariant.objects.create(
                    product=product,
                    sku=variant_data.get('sku'),
                    upc=variant_data.get('upc'),
                    price=variant_data.get('price'),
                    retail_price=variant_data.get('retail_price'),
                    offer_price=variant_data.get('offer_price'),
                    offer_start_time=variant_data.get('offer_start_time'),
                    offer_end_time=variant_data.get('offer_end_time'),
                    stock_quantity=variant_data.get('stock_quantity'),
                    is_active=variant_data.get('is_active', False)
                )

                # Add attributes to the variant
                attributes = variant_data.get('attributes', [])
                for attribute_id in attributes:
                    try:
                        attribute = AttributeValue.objects.get(id=attribute_id)
                        variant.attributes.add(attribute)
                    except AttributeValue.DoesNotExist:
                        continue

                # Handle image upload - match the file name format from frontend
                image_key = f'variant_{index}_image'
                if image_key in request.FILES:
                    variant.image = request.FILES[image_key]
                    variant.save()

                created_variants.append(variant.id)

            return JsonResponse({
                'status': 'success',
                'message': 'Variants created successfully.',
                'variants': created_variants
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid variant data format.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all unique attributes used by this product
        context['product_attributes'] = AttributeValue.objects.all()
        return context
