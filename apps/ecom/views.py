import json
from io import BytesIO

from django.forms import modelformset_factory
from django.views.generic import TemplateView, DetailView, FormView
import barcode
from barcode.writer import ImageWriter
from django_tables2 import SingleTableView
import qrcode
from decouple import config

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy

from apps.helpers import CustomSingleTableMixin, DeleteMessageMixin, MessageMixin, PageHeaderMixin, \
    PermissionRequiredMixin

from .models import (
    Address, Attribute, AttributeValue, Brand, BusinessSetting, Category, Coupon, FlashDeal, Order, Product,
    ProductAttribute,
    ProductImage, ProductVariant, SliderImage, StockEntry, Tag, Tax
)
from .forms import (
    AddressForm, AttributeForm, AttributeValueForm, BrandForm, CategoryForm, CreateCouponForm,
    ProductAttributeForm, ProductForm, ProductImageDirectForm, ProductImageForm,
    ProductVariantForm, SliderImageForm, StockEntryByProductForm, StockEntryForm, TagForm, TaxForm, ProductVariantForm1
)
from .tables import (
    AddressTable, AttributeTable, AttributeValueTable, BrandTable, CategoryTable, CouponTable, FlashDealTable,
    ProductImageTable, ProductTable, ProductVariantTable, SliderImageTable, StockEntryTable, TagTable, TaxTable
)
from .filters import (
    AddressFilter, AttributeFilter, AttributeValueFilter, BrandFilter, CategoryFilter, FlashDealFilter,
    ProductFilter, ProductImageFilter, ProductVariantFilter, StockEntryFilter, TagFilter, TaxFilter
)
from ..promo.models import Hotspot


def generate_barcode(request, stock_entry_id):
    """Generate and save barcode image with product and stock data for a stock entry."""
    stock_entry = get_object_or_404(StockEntry, id=stock_entry_id)

    # If barcode already exists, use the saved image
    if stock_entry.barcode_image:
        return render(request, 'barcode.html', {
            'stock_entry': stock_entry,
            'barcode_image': stock_entry.barcode_image.url,
        })

    # Prepare the data to encode
    data_to_encode = f"Product: {stock_entry.variant.product.name[:15]}, " \
                     f"ID: {stock_entry.id}, Qty: {stock_entry.quantity}"

    # Use Code128 to encode alphanumeric data
    barcode_buffer = BytesIO()
    try:
        code128 = barcode.Code128(data_to_encode, writer=ImageWriter())
        code128.write(barcode_buffer)
    except Exception as e:
        print(f"Error generating barcode: {e}")
    barcode_buffer.seek(0)

    # Save barcode image to the StockEntry model
    barcode_filename = f'barcodes/{stock_entry.id}_barcode.png'
    stock_entry.barcode_image.save(barcode_filename, ContentFile(barcode_buffer.read()), save=False)

    # Save the StockEntry with new barcode image
    stock_entry.save()

    return render(request, 'barcode.html', {
        'stock_entry': stock_entry,
        'barcode_image': stock_entry.barcode_image.url,
    })


class CategoryListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                       FilterView):
    model = Category
    table_class = CategoryTable
    template_name = 'list.html'
    permission_required = 'ecom.view_category'
    filterset_class = CategoryFilter
    # ordering = ['some_field']
    page_title = 'All Categorys'
    add_link = reverse_lazy('category_add')
    add_perms = 'category.add_category'
    edit_perms = 'category.change_category'
    delete_perms = 'category.delete_category'
    edit_url = 'category_update'
    delete_url = 'category_delete'


class CategoryCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add.html'
    permission_required = 'ecom.add_category'
    success_url = reverse_lazy('category_list')
    page_title = 'Category'
    list_link = reverse_lazy('category_list')


class CategoryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add.html'
    permission_required = 'ecom.change_category'
    success_url = reverse_lazy('category_list')
    page_title = 'Update Category'
    list_link = reverse_lazy('category_list')


class CategoryDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Category
    template_name = 'delete.html'
    permission_required = 'ecom.delete_category'
    page_title = 'Delete Category'
    success_url = reverse_lazy('category_list')


class AddressListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Address
    table_class = AddressTable
    template_name = 'list.html'
    permission_required = 'ecom.view_address'
    filterset_class = AddressFilter
    # ordering = ['some_field']
    page_title = 'All Addresss'
    add_link = reverse_lazy('address_add')
    add_perms = 'address.add_address'
    edit_perms = 'address.change_address'
    delete_perms = 'address.delete_address'

    edit_url = 'address_update'
    delete_url = 'address_delete'


class AddressCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'add.html'
    permission_required = 'ecom.add_address'
    success_url = reverse_lazy('address_list')
    page_title = 'Address'
    list_link = reverse_lazy('address_list')


class AddressUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'add.html'
    permission_required = 'ecom.change_address'
    success_url = reverse_lazy('address_list')
    page_title = 'Update Address'
    list_link = reverse_lazy('address_list')


class AddressDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Address
    template_name = 'delete.html'
    permission_required = 'ecom.delete_address'
    page_title = 'Delete Address'
    success_url = reverse_lazy('address_list')


class BrandListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Brand
    table_class = BrandTable
    template_name = 'list.html'
    filterset_class = BrandFilter
    # ordering = ['some_field']
    page_title = 'All Brands'
    add_link = reverse_lazy('brand_add')
    add_perms = 'brand.add_brand'
    edit_perms = 'brand.change_brand'
    delete_perms = 'brand.delete_brand'

    permission_required = 'ecom.view_brand'
    edit_url = 'brand_update'
    delete_url = 'brand_delete'


class BrandCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'add.html'
    permission_required = 'ecom.add_brand'
    success_url = reverse_lazy('brand_list')
    page_title = 'Brand'
    list_link = reverse_lazy('brand_list')


class BrandUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'add.html'
    permission_required = 'ecom.change_brand'
    success_url = reverse_lazy('brand_list')
    page_title = 'Update Brand'
    list_link = reverse_lazy('brand_list')


class BrandDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Brand
    template_name = 'delete.html'
    page_title = 'Delete Brand'
    success_url = reverse_lazy('brand_list')
    permission_required = 'ecom.delete_brand'


# typesense search 
def typesense_demo(request):
    api_key = config('TYPESENSE_KEY')
    api_ip = config('TYPESENSE_IP')
    api_port = config('TYPESENSE_PORT')

    categories = Category.objects.filter(for_product=True)

    context = {
        'api_key': api_key,
        'api_ip': api_ip,
        'api_port': api_port,
        'categories': categories,
    }
    return render(request, 'typesense.html', context)


class AttributeListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                        FilterView):
    model = Attribute
    table_class = AttributeTable
    template_name = 'list.html'
    filterset_class = AttributeFilter
    # ordering = ['some_field']
    page_title = 'All Attributes'
    add_link = reverse_lazy('attribute_add')
    add_perms = 'attribute.add_attribute'
    edit_perms = 'attribute.change_attribute'
    delete_perms = 'attribute.delete_attribute'
    permission_required = 'ecom.view_attribute'
    edit_url = 'attribute_update'
    delete_url = 'attribute_delete'


class AttributeCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Attribute
    form_class = AttributeForm
    template_name = 'add.html'
    success_url = reverse_lazy('attribute_list')
    page_title = 'Attribute'
    list_link = reverse_lazy('attribute_list')
    permission_required = 'ecom.add_attribute'


class AttributeUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Attribute
    form_class = AttributeForm
    template_name = 'add.html'
    success_url = reverse_lazy('attribute_list')
    page_title = 'Update Attribute'
    list_link = reverse_lazy('attribute_list')
    permission_required = 'ecom.change_attribute'


class AttributeDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Attribute
    template_name = 'delete.html'
    page_title = 'Delete Attribute'
    success_url = reverse_lazy('attribute_list')
    permission_required = 'ecom.delete_attribute'


class AttributeValueListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                             FilterView):
    model = AttributeValue
    table_class = AttributeValueTable
    template_name = 'list.html'
    filterset_class = AttributeValueFilter
    # ordering = ['some_field']
    page_title = 'All AttributeValues'
    add_link = reverse_lazy('attributevalue_add')
    add_perms = 'attributevalue.add_attributevalue'
    edit_perms = 'attributevalue.change_attributevalue'
    delete_perms = 'attributevalue.delete_attributevalue'
    permission_required = 'ecom.view_attributevalue'
    edit_url = 'attributevalue_update'
    delete_url = 'attributevalue_delete'


class AttributeValueCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = AttributeValue
    form_class = AttributeValueForm
    template_name = 'add.html'
    success_url = reverse_lazy('attributevalue_list')
    page_title = 'AttributeValue'
    list_link = reverse_lazy('attributevalue_list')
    permission_required = 'ecom.add_attributevalue'


class AttributeValueUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = AttributeValue
    form_class = AttributeValueForm
    template_name = 'add.html'
    success_url = reverse_lazy('attributevalue_list')
    page_title = 'Update AttributeValue'
    list_link = reverse_lazy('attributevalue_list')
    permission_required = 'ecom.change_attributevalue'


class AttributeValueDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin,
                               DeleteView):
    model = AttributeValue
    template_name = 'delete.html'
    page_title = 'Delete AttributeValue'
    success_url = reverse_lazy('attributevalue_list')
    permission_required = 'ecom.delete_attributevalue'


class TagListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Tag
    table_class = TagTable
    template_name = 'list.html'
    filterset_class = TagFilter
    # ordering = ['some_field']
    page_title = 'All Tags'
    add_link = reverse_lazy('tag_add')
    add_perms = 'tag.add_tag'
    edit_perms = 'tag.change_tag'
    delete_perms = 'tag.delete_tag'
    permission_required = 'ecom.view_tag'
    edit_url = 'tag_update'
    delete_url = 'tag_delete'


class TagCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'add.html'
    success_url = reverse_lazy('tag_list')
    page_title = 'Tag'
    list_link = reverse_lazy('tag_list')
    permission_required = 'ecom.add_tag'


class TagUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'add.html'
    success_url = reverse_lazy('tag_list')
    page_title = 'Update Tag'
    list_link = reverse_lazy('tag_list')
    permission_required = 'ecom.change_tag'


class TagDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Tag
    template_name = 'delete.html'
    page_title = 'Delete Tag'
    success_url = reverse_lazy('tag_list')
    permission_required = 'ecom.delete_tag'


class TaxListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Tax
    table_class = TaxTable
    template_name = 'list.html'
    filterset_class = TaxFilter
    # ordering = ['some_field']
    page_title = 'All Taxs'
    add_link = reverse_lazy('tax_add')
    add_perms = 'tax.add_tax'
    edit_perms = 'tax.change_tax'
    delete_perms = 'tax.delete_tax'
    permission_required = 'ecom.view_tax'
    edit_url = 'tax_update'
    delete_url = 'tax_delete'


class TaxCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Tax
    form_class = TaxForm
    template_name = 'add.html'
    success_url = reverse_lazy('tax_list')
    page_title = 'Tax'
    list_link = reverse_lazy('tax_list')
    permission_required = 'ecom.add_tax'


class TaxUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Tax
    form_class = TaxForm
    template_name = 'add.html'
    success_url = reverse_lazy('tax_list')
    page_title = 'Update Tax'
    list_link = reverse_lazy('tax_list')
    permission_required = 'ecom.change_tax'


class TaxDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Tax
    template_name = 'delete.html'
    page_title = 'Delete Tax'
    success_url = reverse_lazy('tax_list')
    permission_required = 'ecom.delete_tax'


class ProductListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = 'list.html'
    filterset_class = ProductFilter
    # ordering = ['some_field']
    page_title = 'All Products'
    add_link = reverse_lazy('product_add')
    add_perms = 'product.add_product'
    edit_perms = 'product.change_product'
    delete_perms = 'product.delete_product'
    permission_required = 'ecom.view_product'
    edit_url = 'product_update'
    delete_url = 'product_delete'


class ProductCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add.html'
    success_url = reverse_lazy('product_list')
    page_title = 'Product'
    list_link = reverse_lazy('product_list')
    permission_required = 'ecom.add_product'

    def form_valid(self, form):
        try:
            # Use transaction.atomic to ensure atomicity
            with transaction.atomic():
                # Save the product instance
                response = super().form_valid(form)

                # Check the 'is_variant' field
                if not self.object.is_variant:
                    # If the product does not have variants, redirect to the product variant update page
                    messages.success(self.request, 'Product added successfully! Please update variant information.')
                    return HttpResponseRedirect(
                        reverse_lazy('productvariant_update', kwargs={'pk': self.object.default_variant.pk}))
                else:
                    messages.success(self.request, 'Product added successfully! Please update variant information.')
                    return HttpResponseRedirect(
                        reverse_lazy('productvariant_bulk', kwargs={'pk': self.object.pk}))

                # Otherwise, follow the normal success URL
                # messages.success(self.request, 'Product added successfully!')
                # return response

        except Exception as e:
            # Handle any exceptions and provide feedback
            messages.error(self.request, f"An error occurred while creating the product: {str(e)}")
            return redirect(self.success_url)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'add.html'
    success_url = reverse_lazy('product_list')
    page_title = 'Update Product'
    list_link = reverse_lazy('product_list')
    permission_required = 'ecom.change_product'


class ProductDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = Product
    template_name = 'delete.html'
    page_title = 'Delete Product'
    success_url = reverse_lazy('product_list')
    permission_required = 'ecom.delete_product'


class ProductAttributeCreateViewDynamic(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, View):
    template_name = 'product_attributes.html'  # Template for rendering the form
    permission_required = 'ecom.add_productattribute'

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')  # Get product_id from URL
        form = ProductAttributeForm()  # Create a blank form
        product = get_object_or_404(Product, pk=product_id)

        # Get existing attributes and values for the product
        product_attributes = ProductAttribute.objects.filter(product=product).prefetch_related('values')

        return render(request, self.template_name, {
            'form': form,
            'product': product,
            'page_title': 'Attributes Values',
            'list_link': reverse_lazy('product_list'),
            'product_attributes': product_attributes,
        })

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')  # Get product_id from URL
        form = ProductAttributeForm(request.POST)  # Create form with POST data

        if form.is_valid():
            attribute = form.cleaned_data['attribute']
            values = form.cleaned_data['values']

            try:
                # Use transaction.atomic to ensure atomicity
                with transaction.atomic():
                    # Fetch the product to ensure it exists
                    product = get_object_or_404(Product, pk=product_id)

                    product_attribute, created = ProductAttribute.objects.get_or_create(
                        product=product,
                        attribute=attribute,
                        defaults={}  # Set initial values if creating
                    )

                    if not created:
                        # Update values, avoiding duplicates
                        existing_values = set(product_attribute.values.all())
                        new_values = set(values)
                        combined_values = existing_values.union(new_values)

                        product_attribute.values.set(combined_values)  # Set unique values
                    else:
                        # If it's a new product attribute, set the values directly
                        product_attribute.values.set(values)  # Correct way to set M2M values

                    product_attribute.save()

                messages.success(self.request, 'Attributes added successfully!')
                success_url = reverse_lazy('product_attribute_dynamic_create', kwargs={'product_id': product_id})
                return redirect(success_url)  # Redirect on success

            except Exception as e:
                messages.error(self.request, f"Error adding attributes: {str(e)}")
                return render(request, self.template_name,
                              {'form': form, 'product_id': product_id, 'page_title': 'Add Attributes Values'})

        return render(request, self.template_name, {'form': form, 'product_id': product_id,
                                                    'page_title': 'Add Attributes Values'})  # Render with errors


@csrf_exempt
@login_required
@permission_required('ecom.delete_productattribute', raise_exception=True)
def delete_product_attribute_values(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attributes = data.get('attributes', {})

            if not attributes:
                return JsonResponse({'success': False, 'error': 'No attributes specified for deletion'}, status=400)

            total_removed = 0
            attribute_deletions = []

            # Use transaction.atomic to ensure atomicity of deletions
            with transaction.atomic():
                # Iterate over each attribute and remove specified values
                for attribute_id, value_ids in attributes.items():
                    product_attribute = ProductAttribute.objects.filter(product__id=product_id,
                                                                        attribute__id=attribute_id).first()

                    if product_attribute is None:
                        print(f"No ProductAttribute found for product_id={product_id} and attribute_id={attribute_id}")
                        continue  # Skip to the next attribute if this one doesn't exist

                    # Remove specified values from the ManyToMany relationship
                    product_attribute.values.remove(*value_ids)
                    total_removed += len(value_ids)

                    # Check if no values remain; if so, delete the ProductAttribute record
                    if not product_attribute.values.exists():
                        product_attribute.delete()
                        attribute_deletions.append(attribute_id)

            return JsonResponse({
                'success': True,
                'total_removed': total_removed,
                'attributes_deleted': attribute_deletions
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


class ProductImageListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                           FilterView):
    model = ProductImage
    table_class = ProductImageTable
    template_name = 'list.html'
    filterset_class = ProductImageFilter
    # ordering = ['some_field']
    page_title = 'All ProductImages'
    add_link = reverse_lazy('productimage_add')
    add_perms = 'productimage.add_productimage'
    edit_perms = 'productimage.change_productimage'
    delete_perms = 'productimage.delete_productimage'
    permission_required = 'ecom.view_productimage'
    edit_url = 'productimage_update'
    delete_url = 'productimage_delete'


class ProductImageCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'add.html'
    success_url = reverse_lazy('productimage_list')
    page_title = 'ProductImage'
    list_link = reverse_lazy('productimage_list')
    permission_required = 'ecom.add_productimage'


class ProductImageUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'add.html'
    success_url = reverse_lazy('productimage_list')
    page_title = 'Update ProductImage'
    list_link = reverse_lazy('productimage_list')
    permission_required = 'ecom.change_productimage'


class ProductImageDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin,
                             DeleteView):
    model = ProductImage
    template_name = 'delete.html'
    page_title = 'Delete ProductImage'
    success_url = reverse_lazy('productimage_list')
    permission_required = 'ecom.delete_productimage'


class ProductImageDirectCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = ProductImage
    form_class = ProductImageDirectForm
    template_name = 'add_product_images.html'
    permission_required = 'ecom.add_productimages'
    edit_url = 'productimage_update'
    delete_url = 'productimage_delete'
    permission_required = 'ecom.add_productimage'

    def get_success_url(self):
        # Access product_id from URL kwargs and return the success URL
        return reverse_lazy('product_add_images', kwargs={'product_id': self.kwargs['product_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        context['product_id'] = product_id
        context['product_images'] = ProductImage.objects.filter(product=product).order_by('-id')
        context['product'] = product
        list_link = reverse_lazy('product_add_images', kwargs={'product_id': product_id})
        context['list_link'] = reverse_lazy('product_list')

        return context

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        form.instance.product = product
        response = super().form_valid(form)

        # Add a success message
        messages.success(self.request, 'Image added successfully!')

        return response


# need to add permission class ACL logic here 
@login_required
@csrf_exempt
@permission_required('ecom.delete_productimage', raise_exception=True)
def delete_product_image(request, image_id):
    if request.method == 'POST':
        try:
            # Use transaction.atomic to ensure both file and record deletion are atomic
            with transaction.atomic():
                # Fetch the image from the database
                image = ProductImage.objects.get(id=image_id)

                # Delete the associated image file
                if image.image:
                    image.image.delete(save=False)  # Delete the image file from storage

                # Delete the image record from the database
                image.delete()

            return JsonResponse({'success': True, 'message': 'Image deleted successfully.'})

        except ProductImage.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Image not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


class ProductVariantListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                             FilterView):
    model = ProductVariant
    table_class = ProductVariantTable
    template_name = 'productvaraint_list.html'
    filterset_class = ProductVariantFilter
    # ordering = ['some_field']
    page_title = 'All Stock'
    add_link = reverse_lazy('productvariant_add')
    add_perms = 'productvariant.add_productvariant'
    edit_perms = 'productvariant.change_productvariant'
    permission_required = 'ecom.view_productvariant'
    edit_url = 'productvariant_update'
    delete_url = 'productvariant_delete'

    def calculate_financial_metrics(self):
        """
        Calculate financial metrics for all product variants.
        Returns a dictionary with metrics.
        """
        queryset = self.get_queryset()

        closing_stock_purchase_price = sum(
            variant.price * variant.stock_quantity for variant in queryset
        )
        closing_stock_sale_price = sum(
            variant.calculate_retail_price() * variant.stock_quantity for variant in queryset
        )
        potential_profit = closing_stock_sale_price - closing_stock_purchase_price
        profit_margin = (
            (potential_profit / closing_stock_sale_price) * 100
            if closing_stock_sale_price > 0
            else 0
        )

        return {
            "closing_stock_purchase_price": closing_stock_purchase_price,
            "closing_stock_sale_price": closing_stock_sale_price,
            "potential_profit": potential_profit,
            "profit_margin": profit_margin,
        }

    def get_context_data(self, **kwargs):
        """
        Add financial metrics to the context data.
        """
        context = super().get_context_data(**kwargs)
        metrics = self.calculate_financial_metrics()
        context.update(metrics)
        return context

    # delete_perms = 'productvariant.delete_productvariant'


class ProductVariantCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = 'productvariant_add.html'
    success_url = reverse_lazy('productvariant_list')
    page_title = 'Stock'
    list_link = reverse_lazy('productvariant_list')
    permission_required = 'ecom.add_productvariant'

    def form_valid(self, form):
        with transaction.atomic():
            # Save the ProductVariant with stock_quantity initialized to zero
            product_variant = form.save(commit=False)
            product_variant.stock_quantity = 0
            product_variant.save()
            form.save_m2m()  # Save many-to-many relationships

            # Get the initial_stock_quantity from the form
            initial_quantity = form.cleaned_data.get('initial_stock_quantity', 0)
            if initial_quantity and initial_quantity > 0:
                # Create a StockEntry to represent the initial stock
                StockEntry.objects.create(
                    variant=product_variant,
                    quantity=initial_quantity,
                    change_type='adjustment',
                    adjustment_direction='increase',
                    notes='Initial stock entry upon creation of the product variant.',
                )
            messages.success(self.request, 'Product variant created successfully.')

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['list_link'] = self.list_link
        return context

    def get_success_url(self):
        return f"{reverse_lazy('productvariant_list')}?product={self.object.product.pk}"


class ProductVariantUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = 'productvariant_add.html'
    success_url = reverse_lazy('productvariant_list')
    page_title = 'Update Stock'
    list_link = reverse_lazy('productvariant_list')
    permission_required = 'ecom.change_productvariant'

    def get_form_class(self):
        if self.object.product.is_variant:
            return ProductVariantForm
        else:
            return ProductVariantForm1

    def form_valid(self, form):
        messages.success(self.request, 'Product variant updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse_lazy('productvariant_list')}?product={self.object.product.pk}"


class ProductVariantDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin,
                               DeleteView):
    model = ProductVariant
    template_name = 'delete.html'
    page_title = 'Delete Stock'
    success_url = reverse_lazy('productvariant_list')
    permission_required = 'ecom.change_productvariant'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product variant deleted successfully.')
        return super().delete(request, *args, **kwargs)


class StockEntryListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin,
                         FilterView):
    model = StockEntry
    table_class = StockEntryTable
    template_name = 'list.html'
    filterset_class = StockEntryFilter
    # ordering = ['some_field']
    page_title = 'All Stock Entrys'
    add_link = reverse_lazy('stockentry_add')
    add_perms = 'stockentry.add_stockentry'
    # edit_perms = 'stockentry.change_stockentry'
    # delete_perms = 'stockentry.delete_stockentry'
    permission_required = 'ecom.view_stockentry'
    edit_url = 'stockentry_update'
    delete_url = 'stockentry_delete'


class StockEntryCreateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, CreateView):
    model = StockEntry
    form_class = StockEntryForm
    template_name = 'add.html'
    success_url = reverse_lazy('stockentry_list')
    page_title = 'Stock Entry'
    list_link = reverse_lazy('stockentry_list')
    permission_required = 'ecom.add_stockentry'

    def form_valid(self, form):
        messages.success(self.request, 'Stock entry created successfully.')
        return super().form_valid(form)


class StockEntryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, MessageMixin, UpdateView):
    model = StockEntry
    form_class = StockEntryForm
    template_name = 'add.html'
    success_url = reverse_lazy('stockentry_list')
    page_title = 'Update Stock Entry'
    list_link = reverse_lazy('stockentry_list')
    permission_required = 'ecom.change_stockentry'

    def form_valid(self, form):
        messages.success(self.request, 'Stock entry updated successfully.')
        return super().form_valid(form)


class StockEntryDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin,
                           DeleteView):
    model = StockEntry
    template_name = 'delete.html'
    page_title = 'Delete Stock Entry'
    success_url = reverse_lazy('stockentry_list')
    permission_required = 'ecom.delete_stockentry'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Stock entry deleted successfully.')
        return super().delete(request, *args, **kwargs)


class StockUpdateByProductViewDynamic(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, View):
    template_name = 'direct_stock_add.html'
    permission_required = 'ecom.change_stockentry'

    def get(self, request, *args, **kwargs):
        variant_id = self.kwargs.get('variant_id')  # Get variant_id from URL
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        stock_entries = StockEntry.objects.filter(variant=variant).order_by('-timestamp')
        form = StockEntryByProductForm()
        return render(request, self.template_name, {
            'form': form,
            'variant': variant,
            'stock_entries': stock_entries,
            'page_title': 'Stock for Variant',
            'list_link': reverse_lazy('product_list'),
        })

    def post(self, request, *args, **kwargs):
        variant_id = self.kwargs.get('variant_id')  # Get variant_id from URL
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        form = StockEntryByProductForm(request.POST)

        if form.is_valid():
            try:
                # Use transaction.atomic to ensure atomicity
                with transaction.atomic():
                    # Create a new StockEntry instance
                    stock_entry = StockEntry(
                        variant=variant,
                        quantity=form.cleaned_data['quantity'],
                        change_type=form.cleaned_data['change_type'],
                        adjustment_direction=form.cleaned_data.get('adjustment_direction'),
                        notes=form.cleaned_data.get('notes'),
                    )
                    stock_entry.save()

                messages.success(request, 'Stock entry added successfully!')
                success_url = reverse_lazy('productvariant_list')
                return redirect(success_url)

            except Exception as e:
                # Handle any errors that occur during the save process
                messages.error(request, f"An error occurred: {str(e)}")

        # If form is not valid or an exception occurred, re-render the form with errors
        stock_entries = StockEntry.objects.filter(variant=variant).order_by('-timestamp')
        return render(request, self.template_name, {
            'form': form,
            'variant': variant,
            'stock_entries': stock_entries,
            'page_title': 'Update Stock for Variant',
            'list_link': reverse_lazy('product_list'),
        })


from django.contrib.auth.mixins import UserPassesTestMixin


class CreateCouponView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Coupon
    form_class = CreateCouponForm
    template_name = 'create_coupon.html'
    success_url = reverse_lazy('coupon-list')

    def test_func(self):
        # Check if the user is staff or admin
        return self.request.user.is_staff or self.request.user.is_superuser


class CouponListView(SingleTableView):
    model = Coupon
    table_class = CouponTable
    template_name = 'coupon_list.html'
    context_object_name = 'coupons'


class SliderImageListView(LoginRequiredMixin, UserPassesTestMixin, SingleTableView):
    model = SliderImage
    table_class = SliderImageTable
    template_name = 'slider_image_list.html'
    context_object_name = 'slider_images'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class SliderImageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SliderImage
    form_class = SliderImageForm
    template_name = 'slider_image_form.html'
    success_url = reverse_lazy('slider_image_list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Slider image added successfully!")
        return super().form_valid(form)


class SliderImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SliderImage
    form_class = SliderImageForm
    template_name = 'slider_image_form.html'
    success_url = reverse_lazy('slider_image_list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Slider image updated successfully!")
        return super().form_valid(form)


class SliderImageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'ecom.delete_sliderimage'

    def post(self, request, pk):
        slider_image = get_object_or_404(SliderImage, pk=pk)
        slider_image.delete()
        messages.success(request, "Slider image deleted successfully.")
        return redirect(reverse_lazy('slider_image_list'))


from .models import Order

from .forms import OrderForm

from .tables import OrderTable

from .filters import OrderFilter


class OrderListView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = Order
    ordering = ['-created_at']
    table_class = OrderTable
    template_name = 'list.html'
    filterset_class = OrderFilter
    # ordering = ['some_field']
    page_title = 'All Orders'
    add_link = reverse_lazy('order_add')
    add_perms = 'order.add_order'
    edit_perms = 'order.change_order'
    # delete_perms = 'order.delete_order'

    permission_required = 'ecom.view_order'
    edit_url = 'order_update'
    # delete_url = 'order_delete'


class OrderCreateView(LoginRequiredMixin, PageHeaderMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'add.html'
    success_url = reverse_lazy('order_list')
    page_title = 'Order'
    list_link = reverse_lazy('order_list')


class OrderUpdateView(LoginRequiredMixin, PageHeaderMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'add.html'
    success_url = reverse_lazy('order_list')
    page_title = 'Update Order'
    list_link = reverse_lazy('order_list')


class OrderDeleteView(LoginRequiredMixin, PageHeaderMixin, DeleteView):
    model = Order
    template_name = 'delete.html'
    page_title = 'Delete Order'
    success_url = reverse_lazy('order_list')


import time
from django.http import StreamingHttpResponse
from django.core.management import call_command
from django.core.management.base import CommandError


def reindex_view(request):
    def reindex_generator():
        yield "Starting reindexing process...\n"
        try:
            # Call the management command directly
            call_command("typesense_products", "reindex")  # Replace 'typesense_products' with your command name
            yield "Reindexing completed successfully.\n"
        except CommandError as e:
            yield f"Error occurred: {str(e)}\n"
        yield "Done.\n"

    # Stream the response to the client
    return StreamingHttpResponse(reindex_generator(), content_type="text/plain")


# add menu

class ManageMenuView(PermissionRequiredMixin, TemplateView):
    template_name = "manage_menu.html"
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all categories
        categories = Category.objects.filter(is_active=True, for_product=True)
        context['categories'] = categories

        # Get current menu categories from the Setting model
        menu_setting = BusinessSetting.objects.filter(key='menu_categories').first()
        if menu_setting and menu_setting.value:
            try:
                # Convert the comma-separated string into a list of integers
                menu_category_ids = [int(cat_id) for cat_id in menu_setting.value.split(',')]
                context['menu_categories'] = Category.objects.filter(id__in=menu_category_ids, is_active=True, for_product=True)
            except ValueError:
                context['menu_categories'] = []  # Handle invalid data gracefully
        else:
            context['menu_categories'] = []

        return context


from django.contrib.auth.mixins import PermissionRequiredMixin


#
# class ManageMenuView(PermissionRequiredMixin, TemplateView):
#     template_name = "manage_menu.html"
#     permission_required = 'is_staff'  # Only staff members can access
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Get all categories
#         categories = Category.objects.filter(is_active=True)
#         context['categories'] = categories
#
#         # Get current menu categories from the Setting model
#         menu_setting = BusinessSetting.objects.filter(key='menu_categories').first()
#         if menu_setting and menu_setting.value:
#             try:
#                 # Convert the comma-separated string into a list of integers
#                 menu_category_ids = [int(cat_id) for cat_id in menu_setting.value.split(',')]
#                 context['menu_categories'] = Category.objects.filter(id__in=menu_category_ids, is_active=True)
#             except ValueError:
#                 context['menu_categories'] = []  # Handle invalid data gracefully
#         else:
#             context['menu_categories'] = []
#
#         return context

class ManageMenuView(PermissionRequiredMixin, TemplateView):
    template_name = "category_setting.html"  # Update to your new template name
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all categories
        categories = Category.objects.filter(is_active=True, for_product=True)
        context['categories'] = categories
        context['hotspot_list'] = Hotspot.objects.all()

        # Get menu categories
        menu_setting = BusinessSetting.objects.filter(key='menu_categories').first()
        if menu_setting and menu_setting.value:
            try:
                menu_category_ids = [int(cat_id) for cat_id in menu_setting.value.split(',')]
                context['menu_categories'] = Category.objects.filter(id__in=menu_category_ids, is_active=True, for_product=True)
            except ValueError:
                context['menu_categories'] = []
        else:
            context['menu_categories'] = []

        # Get unique collections
        collection_setting = BusinessSetting.objects.filter(key='unique_collection').first()
        if collection_setting and collection_setting.value:
            try:
                collection_category_ids = [int(cat_id) for cat_id in collection_setting.value.split(',')]
                context['unique_collections'] = Category.objects.filter(id__in=collection_category_ids, for_product=True, is_active=True)
            except ValueError:
                context['unique_collections'] = []
        else:
            context['unique_collections'] = []

        # Get unique collections
        inspiration_setting = BusinessSetting.objects.filter(key='inspiration_collection').first()
        if inspiration_setting and inspiration_setting.value:
            try:
                inspiration_category_ids = [int(cat_id) for cat_id in inspiration_setting.value.split(',')]
                context['inspiration_collections'] = Category.objects.filter(id__in=inspiration_category_ids, for_product=True,
                                                                             is_active=True)
            except ValueError:
                context['inspiration_collections'] = []
        else:
            context['inspiration_collections'] = []

        # Get banner settings
        banner_settings = BusinessSetting.objects.filter(key='home_banner_settings').first()
        if banner_settings and banner_settings.value:
            try:
                context['banner_settings'] = banner_settings
            except json.JSONDecodeError:
                context['banner_settings'] = {}
        else:
            context['banner_settings'] = {}

        return context


from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
@csrf_exempt  # Allow requests without CSRF token for simplicity (use sparingly)
def save_menu_categories(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from the request body
            category_ids = data.get('category_ids', [])
            key_name = data.get('key_name')
            if not key_name and not category_ids:
                return JsonResponse({'status': 'error', 'message': 'Please provide category ids and key_name.'})

            # Save or update the BusinessSetting key
            menu_setting, created = BusinessSetting.objects.get_or_create(key=key_name)
            menu_setting.value = ','.join(map(str, category_ids))  # Save IDs as a comma-separated string
            menu_setting.save()

            return JsonResponse({'success': True, 'message': 'Menu categories updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@staff_member_required
def save_banner_settings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            settings_data = {
                'title': data.get('title', ''),
                'gallery_id': data.get('gallery_id', '')
            }

            # Save banner settings
            banner_settings, created = BusinessSetting.objects.get_or_create(
                key='home_banner_settings'
            )
            banner_settings.value = settings_data  # Direct assignment since it's JSONField
            banner_settings.save()

            return JsonResponse({
                'success': True,
                'message': 'Banner settings saved successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })


# flash deal

class FlashDealView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, CustomSingleTableMixin, FilterView):
    model = FlashDeal
    table_class = FlashDealTable
    template_name = 'list.html'
    filterset_class = FlashDealFilter
    # ordering = ['some_field']
    page_title = 'Flass Deals'
    add_link = reverse_lazy('flash_deal_create')
    add_perms = 'flashdeal.add_flashdeal'
    edit_perms = 'flashdeal.change_flashdeal'
    delete_perms = 'flashdeal.delete_flashdeal'
    permission_required = 'ecom.view_flashdeal'
    edit_url = 'flash_deal_edit'
    delete_url = 'flash_deals_delete'


class FlashDealDeleteView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, DeleteMessageMixin, DeleteView):
    model = FlashDeal
    template_name = 'delete.html'
    page_title = 'Delete Flash Deal'
    success_url = reverse_lazy('flash_deals')
    permission_required = 'ecom.delete_flashdeal'


class FlashDealCreateEditView(PermissionRequiredMixin, LoginRequiredMixin, PageHeaderMixin, View):
    success_url = reverse_lazy('flash_deals')
    page_title = 'Flash Deal'
    list_link = reverse_lazy('flash_deals')
    permission_required = 'ecom.add_flashdeal'

    def get(self, request, flash_deal_id=None):
        """
        Render the Flash Deal form page for create or edit.
        """
        flash_deal_json = 'null'
        banner_image_url = None
        if flash_deal_id:
            flash_deal = get_object_or_404(FlashDeal, pk=flash_deal_id)
            # Prepare the flash deal data, including banner image URL if needed
            flash_deal_data = {
                'id': flash_deal.id,
                'title': flash_deal.title,
                'description': flash_deal.description,
                'startDate': flash_deal.start_date.strftime('%Y-%m-%dT%H:%M'),
                'endDate': flash_deal.end_date.strftime('%Y-%m-%dT%H:%M'),
                'variants': flash_deal.product_variants or '[]',
                'is_active': flash_deal.is_active,

            }
            # If you want to include the banner image URL

            if flash_deal.banner_image:
                flash_deal_data['banner_image_url'] = flash_deal.banner_image.url
                banner_image_url = flash_deal.banner_image.url

            flash_deal_json = json.dumps(flash_deal_data)

        return render(request, 'flash_deal_form.html', {
            'flash_deal_json': flash_deal_json,
            'flash_deal_id': flash_deal_id or 'create',
            'banner_image': banner_image_url or None,
        })

    @method_decorator(csrf_exempt)
    def post(self, request, flash_deal_id=None):
        """
        Handle creating or updating a Flash Deal.
        """
        try:
            # Handle file upload and form data
            data = request.POST
            title = data.get('title')
            description = data.get('description')
            start_date = data.get('startDate')
            end_date = data.get('endDate')

            variants_json = data.get('variants', '[]')
            variants = json.loads(variants_json)
            banner_image = request.FILES.get('banner_image')
            is_active = request.POST.get('is_active', 'false').lower() == 'true'

            if flash_deal_id and flash_deal_id != 'create':
                # Edit an existing Flash Deal
                flash_deal = get_object_or_404(FlashDeal, pk=flash_deal_id)
                flash_deal.title = title
                flash_deal.description = description
                flash_deal.start_date = start_date
                flash_deal.end_date = end_date
                flash_deal.is_active = is_active
                if banner_image:
                    flash_deal.banner_image = banner_image
                flash_deal.save()
            else:
                # Create a new Flash Deal
                flash_deal = FlashDeal.objects.create(
                    title=title,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    banner_image=banner_image if banner_image else None,
                )

            # Update variants
            flash_deal_variants = []
            for variant_data in variants:
                variant_id = variant_data.get('id')
                offer_price = variant_data.get('offerPrice')

                variant = get_object_or_404(ProductVariant, pk=variant_id)
                variant.offer_price = offer_price
                variant.offer_start_time = start_date
                variant.offer_end_time = end_date
                variant.save()

                flash_deal_variants.append({
                    'id': variant.id,
                    'name': variant.product.name,
                    'price': str(variant.price),
                    'offerPrice': str(variant.offer_price),
                    'retailPrice': str(variant.retail_price),

                })

            flash_deal.product_variants = flash_deal_variants
            flash_deal.save()

            return JsonResponse({'message': 'Flash deal saved successfully.', 'id': flash_deal.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class VariantSearchView(View):
    def get(self, request):
        """
        Search and return ProductVariant objects for the dropdown.
        """
        search_query = request.GET.get('search', '')
        variants = ProductVariant.objects.filter(
            is_active=True,
            product__name__icontains=search_query
        )[:10]  # Limit to 10 results for performance

        return JsonResponse({
            'results': [
                {
                    'id': variant.id,
                    'name': variant.product.name,
                    'price': str(variant.price),
                    'retail_price': str(variant.retail_price),
                }
                for variant in variants
            ]
        })


from apps.ecom.models import CustomUser
from django.db import models


def get_dashboard_data(request):
    # Aggregate the data dynamically
    total_sales = Order.objects.filter(status="delivered").aggregate(total=models.Sum('total_amount'))['total'] or 0
    total_orders = Order.objects.count()
    total_customers = CustomUser.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()

    # Fetch recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5].values(
        'id', 'user__name', 'created_at', 'status', 'total_amount'
    )
    for order in recent_orders:
        order['total_amount'] = float(order['total_amount']) if order['total_amount'] else 0.0
    return JsonResponse({
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_products': total_products,
        'recent_orders': list(recent_orders),
    })


@login_required
@permission_required('ecom.view_order', raise_exception=True)
def order_detail_json(request, pk):
    """
    Return JSON representation of an Order and its lines for modal display.
    """
    try:
        order = get_object_or_404(Order, pk=pk)
        # order basic info
        order_data = {
            'id': order.id,
            'user': getattr(order.user, 'username', None) or getattr(order.user, 'name', None),
            'status': order.status,
            'payment_status': order.payment_status,
            'subtotal': str(order.subtotal),
            'shipping_cost': str(order.shipping_cost),
            'total_discount': str(order.total_discount),
            'total_amount': str(order.total_amount),
            'notes': order.notes,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'updated_at': order.updated_at.isoformat() if order.updated_at else None,
            'shipping_method': order.shipping_method.name if order.shipping_method else None,
            'coupon': order.coupon.code if order.coupon else None,
        }

        # addresses
        if order.shipping_address:
            order_data['shipping_address'] = {
                'id': order.shipping_address.id,
                'display': str(order.shipping_address)
            }
        else:
            order_data['shipping_address'] = None

        if order.billing_address:
            order_data['billing_address'] = {
                'id': order.billing_address.id,
                'display': str(order.billing_address)
            }
        else:
            order_data['billing_address'] = None

        # order lines
        lines = []
        for ol in order.order_lines.all():
            lines.append({
                'id': ol.id,
                'variant_id': ol.variant.id if ol.variant else None,
                'product_name': ol.product_name,
                'sku': ol.sku,
                'quantity': ol.quantity,
                'price': str(ol.price),
                'discount': str(ol.discount),
                'final_price': str(ol.final_price),
                'total_price': str(ol.total_price),
            })
        order_data['order_lines'] = lines

        # available choices for front-end selects (list of [value,label])
        order_field = Order._meta.get_field('status')
        order_choices = list(order_field.choices)

        payment_field = Order._meta.get_field('payment_status')
        payment_choices = list(payment_field.choices)

        order_data['available_statuses'] = order_choices
        order_data['available_payment_statuses'] = payment_choices

        return JsonResponse(order_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
@permission_required('ecom.change_order', raise_exception=True)
def order_update_status(request, pk):
    """
    Accept JSON payload with keys: status, payment_status, notes
    Update the order accordingly and return updated order data.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        order = get_object_or_404(Order, pk=pk)
        payload = json.loads(request.body.decode('utf-8') or "{}")

        new_status = payload.get('status')
        new_payment_status = payload.get('payment_status')
        new_notes = payload.get('notes')

        # validate status against choices
        status_field = Order._meta.get_field('status')
        valid_statuses = [c[0] for c in status_field.choices]
        if new_status and new_status not in valid_statuses:
            return JsonResponse({'error': 'Invalid status value'}, status=400)

        payment_field = Order._meta.get_field('payment_status')
        valid_payments = [c[0] for c in payment_field.choices]
        if new_payment_status and new_payment_status not in valid_payments:
            return JsonResponse({'error': 'Invalid payment_status value'}, status=400)

        updated = False
        if new_status and new_status != order.status:
            order.status = new_status
            updated = True
        if new_payment_status and new_payment_status != order.payment_status:
            order.payment_status = new_payment_status
            updated = True
        if new_notes is not None and new_notes != order.notes:
            order.notes = new_notes
            updated = True

        if updated:
            order.save()

        # Return updated minimal payload
        return JsonResponse({
            'success': True,
            'id': order.id,
            'status': order.status,
            'payment_status': order.payment_status,
            'notes': order.notes
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

