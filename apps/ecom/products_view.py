# views.py

from django.shortcuts import render, redirect
from django.views import View
from .forms import ProductForm, ProductVariantForm
from .models import Product, ProductVariant, Attribute, AttributeValue
from django.http import JsonResponse
import json

class ProductCreateView2(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'product_create.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            has_variants = form.cleaned_data.get('has_variants')
            attributes = form.cleaned_data.get('attributes')
            product.save()
            form.save_m2m()  # Save many-to-many relationships like tags

            if has_variants:
                # Handle variants data from form
                variants_data = request.POST.get('variants_data')
                if variants_data:
                    variants = json.loads(variants_data)
                    for variant_data in variants:
                        sku = variant_data.get('sku')
                        price = variant_data.get('price')
                        retail_price = variant_data.get('retail_price') or None
                        stock_quantity = variant_data.get('stock_quantity')
                        is_active = variant_data.get('is_active', True)
                        attribute_value_ids = variant_data.get('attribute_value_ids')
                        variant = ProductVariant.objects.create(
                            product=product,
                            sku=sku,
                            price=price,
                            retail_price=retail_price,
                            is_active=is_active,
                            stock_quantity=stock_quantity
                        )
                        if attribute_value_ids:
                            attribute_values = AttributeValue.objects.filter(id__in=attribute_value_ids)
                            variant.attributes.set(attribute_values)
            else:
                # Create a default variant
                sku = product.slug
                price = request.POST.get('price')
                retail_price = request.POST.get('retail_price') or None
                stock_quantity = request.POST.get('stock_quantity')
                variant = ProductVariant.objects.create(
                    product=product,
                    sku=sku,
                    price=price,
                    retail_price=retail_price,
                    is_active=True,
                    stock_quantity=stock_quantity
                )
            # return redirect('product_detail', pk=product.pk)
            return redirect('add_product')
        return render(request, 'product_create.html', {'form': form})

# AJAX endpoint to get attribute values
def get_attribute_values(request):
    attribute_ids = request.GET.get('attribute_ids', '')
    if attribute_ids:
        ids = attribute_ids.split(',')
        attributes = Attribute.objects.filter(id__in=ids)
        data = []
        for attribute in attributes:
            values = attribute.values.all()
            value_list = [{'id': v.id, 'value': v.value} for v in values]
            data.append({
                'attribute': {'id': attribute.id, 'name': attribute.name},
                'values': value_list
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)
