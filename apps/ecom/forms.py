from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit, Div, HTML
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.forms.widgets import DateTimeInput

from apps.ecom.mixins import AttributeValueWidget, AttributeWidget, CategoryWidget, BrandWidget, \
    TagMultipleSelect2Widget
from apps.lookup import CustomSelect2Mixin
from .models import AttributeValue, Coupon, Order, Product, ProductAttribute, ProductImage, ProductVariant, Attribute, \
    StockEntry, SupportTicket, SupportTicketMessage, Tag, Category, Tax


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name', 'parent', 'image', 'icon', 'description', 'meta_title', 'meta_description', 'slug', 'is_featured',
            'is_active', 'for_product', 'for_solution')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'parent', 'image', 'icon', 'description'),
            ),
            HTML(
                """
    <div>
        <button type="button" id="generate-meta" class="btn btn-secondary mb-3">
            Generate Meta Title, and Description using AI
        </button>
        <p id="validation-warning" style="color: red; display: none; font-size: 14px; margin-top: 5px;">
            * Product Name and Description are required to generate meta content.
        </p>
    </div>
    <script>
        document.getElementById('generate-meta').addEventListener('click', function () {
            // Get the values from the form fields
            const name = document.getElementById('id_name').value.trim();
            const description = document.getElementById('id_description').value.trim();
            const parent = document.getElementById('id_parent').options[document.getElementById('id_parent').selectedIndex].text;

            const warningElement = document.getElementById('validation-warning');

            // Validate mandatory fields (Name and Description)
            if (!name || !description) {
                warningElement.style.display = 'block';
                return; // Stop the request if validation fails
            }

            // Hide the warning if validation passes
            warningElement.style.display = 'none';

            // Disable the button while processing
            const button = this;
            button.textContent = 'Generating...';
            button.disabled = true;

            // Perform an AJAX request
            fetch("{% url 'generate_meta_category' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    parent: parent
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Fill in the meta title and description fields
                document.getElementById('id_meta_title').value = data.meta_title;
                document.getElementById('id_meta_description').value = data.meta_description;

                // Reset button state
                button.textContent = 'Generate Meta Title, and Description using AI';
                button.disabled = false;
            })
            .catch(error => {
                console.error('Error generating meta data:', error);
                alert('Failed to generate meta data. Please try again.');

                // Reset button state
                button.textContent = 'Generate Meta Title, and Description using AI';
                button.disabled = false;
            });
        });
    </script>
                """
            ),
            Row(
                Column('meta_title', 'meta_description', 'slug', 'is_featured', 'is_active', 'for_product', 'for_solution'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )

        )

class CategoryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-2 mb-0'),
                Column('parent', css_class='form-group col-md-2 mb-0'),
                Column('is_featured', css_class='form-group col-md-2 mb-0'),
                Column('for_product', css_class='form-group col-md-2 mb-0'),
                Column('for_solution', css_class='form-group col-md-2 mb-0'),
                Column('is_active', css_class='form-group col-md-1 mb-0'),
                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'user', 'full_name', 'address_line_1', 'address_line_2', 'city', 'state_or_province', 'postal_code',
            'country',
            'phone_number', 'is_default_shipping', 'is_default_billing',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user', 'full_name', 'address_line_1', 'address_line_2', 'city', 'state_or_province',
                       'postal_code', 'country', 'phone_number', 'is_default_shipping', 'is_default_billing'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class AddressFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-4 mb-0'),
                Column('full_name', css_class='form-group col-md-4 mb-0'),
                Column('address_line_1', css_class='form-group col-md-4 mb-0'),
                Column('address_line_2', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state_or_province', css_class='form-group col-md-4 mb-0'),
                Column('postal_code', css_class='form-group col-md-4 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
                Column('is_default_shipping', css_class='form-group col-md-4 mb-0'),
                Column('is_default_billing', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


from .models import Brand


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'logo', 'description', 'meta_title', 'meta_description', 'slug', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'logo', 'description', 'meta_title', 'meta_description', 'slug', 'is_active'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class BrandFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),

                Column('description', css_class='form-group col-md-4 mb-0'),
                Column('meta_title', css_class='form-group col-md-4 mb-0'),
                Column('meta_description', css_class='form-group col-md-4 mb-0'),
                Column('slug', css_class='form-group col-md-4 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


# class ProductVariantForm(forms.ModelForm):
#     class Meta:
#         model = ProductVariant
#         fields = ['sku', 'price', 'retail_price', 'is_active', 'attributes', 'image', 'stock_quantity']

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = (
            'name',
            'parent',  # <-- Include parent here
            'data_type',
            'unit',
            'is_filterable',
            'is_variation',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                # Show 'name' and 'parent' side by side, for example
                Column('name', css_class='col-md-6 mb-0'),
                Column('parent', css_class='col-md-6 mb-0'),
            ),
            Row(
                Column('data_type', 'unit', 'is_filterable', 'is_variation'),
            ),
            Row(
                Column(
                    Submit(
                        'submit', 'Save',
                        css_class='btn btn-primary',
                        onclick="return confirm('Are you sure you want to submit?');"
                    )
                ),
            )
        )


# class AttributeForm(forms.ModelForm):
#     class Meta:
#         model = Attribute
#         fields = ('name', 'data_type', 'unit', 'is_filterable', 'is_variation',)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('name', 'data_type', 'unit', 'is_filterable', 'is_variation'),
#             ),
#             Row(
#                 Column(
#                    Submit('submit', 'Save', css_class='btn btn-primary',               onclick="return confirm('Are you sure you want to submit?');")
#                 ),
#             )
#         )

class AttributeFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('data_type', css_class='form-group col-md-4 mb-0'),
                Column('unit', css_class='form-group col-md-4 mb-0'),
                Column('is_filterable', css_class='form-group col-md-4 mb-0'),
                Column('is_variation', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ('attribute', 'value',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('attribute', 'value'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class AttributeValueFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('attribute', css_class='form-group col-md-4 mb-0'),
                Column('value', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary mt-3',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class TagFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ('name', 'value', 'tax_type', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'value', 'tax_type', 'is_active'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class TaxFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('tax_type', css_class='form-group col-md-2 mb-0'),
                Column('is_active', css_class='form-group col-md-2 mb-0'),

                Column(HTML("""<button class='btn btn-sm btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-2 mb-0 mt-6'),
            ),

        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name', 'category', 'brand', 'is_variant', 'is_featured', 'unit', 'min_order_quantity',
            'max_order_quantity', 'description', 'key_features', 'meta_title', 'meta_description',
            'is_active', 'warranty', 'tags', 'is_saleable'
        )
        exclude = ['slug']
        widgets = {
            'description': SummernoteWidget(),
            # 'category': CategoryWidget(attrs={
            #     'data-minimum-input-length': 0,
            #     'class': 'form-control select2-widget'
            # }),
            # 'key_features': SummernoteWidget(),
            # 'category': CategoryWidget(attrs={
            #     'data-minimum-input-length': 0,
            #     'class': 'form-control select2-widget'
            # }),
            'brand': BrandWidget(attrs={
                'data-minimum-input-length': 0,
                'class': 'form-control select2-widget'
            }),
            'tags': TagMultipleSelect2Widget(attrs={
                'data-minimum-input-length': 0,
                'class': 'form-control select2-widget'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        # Enhancing layout with well-structured rows and columns
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('category', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('brand', css_class='form-group col-md-6 mb-3'),
                Column('unit', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('is_variant', css_class='form-group col-md-4 mb-3'),
                Column('is_featured', css_class='form-group col-md-4 mb-3'),  # Add is_featured here
                Column('is_saleable', css_class='form-group col-md-4 mb-3'),  # Add is_featured here
            ),
            Row(
                Column('warranty', css_class='form-group col-md-6 mb-3'),
                Column('min_order_quantity', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('max_order_quantity', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-4'),
            ),
            Row(
                Column('key_features', css_class='form-group col-md-12 mb-4'),
            ),

            # Tag Section
            HTML('<h2 class="mt-3">Tags & SEO</h2>'),
            # Row(
            #     Column('tags', css_class='form-group col-md-12 mb-3'),
            # ),
            Row(
                Column('tags', css_class='form-group col-md-12 mb-3'),
            ),
            HTML(
                """
                <div>
                    <button type="button" id="generate-meta" class="btn btn-secondary mb-3">
                        Generate Meta Title, and Description using AI
                    </button>
                    <p id="validation-warning" style="color: red; display: none; font-size: 14px; margin-top: 5px;">
                        * Product Name and Description are required to generate meta content.
                    </p>
                </div>
                <script>
                    document.getElementById('generate-meta').addEventListener('click', function () {
                        // Get the values from the form fields
                        const name = document.getElementById('id_name').value.trim();
                        const description = document.getElementById('id_description').value.trim();
                        const keyFeatures = document.getElementById('id_key_features').value.trim();
                        const category = document.getElementById('id_category').options[document.getElementById('id_category').selectedIndex].text;
                        const brand = document.getElementById('id_brand').options[document.getElementById('id_brand').selectedIndex].text;
                        const warranty = document.getElementById('id_warranty').value.trim();
            
                        const warningElement = document.getElementById('validation-warning');
            
                        // Validate mandatory fields (Name and Description)
                        if (!name || !description) {
                            warningElement.style.display = 'block';
                            return; // Stop the request if validation fails
                        }
            
                        // Hide the warning if validation passes
                        warningElement.style.display = 'none';
            
                        // Disable the button while processing
                        const button = this;
                        button.textContent = 'Generating...';
                        button.disabled = true;
            
                        // Perform an AJAX request
                        fetch("{% url 'generate_meta' %}", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": "{{ csrf_token }}",
                            },
                            body: JSON.stringify({
                                name: name,
                                description: description,
                                key_features: keyFeatures,
                                category: category,
                                brand: brand,
                                warranty: warranty
                            }),
                        })
                        .then(response => response.json())
                        .then(data => {
                            // Fill in the meta title and description fields
                            document.getElementById('id_meta_title').value = data.meta_title;
                            document.getElementById('id_meta_description').value = data.meta_description;
            
                            // Reset button state
                            button.textContent = 'Generate Meta Title, and Description using AI';
                            button.disabled = false;
                        })
                        .catch(error => {
                            console.error('Error generating meta data:', error);
                            alert('Failed to generate meta data. Please try again.');
            
                            // Reset button state
                            button.textContent = 'Generate Meta Title, and Description using AI';
                            button.disabled = false;
                        });
                    });
                </script>
                """
            ),

            Row(
                Column('meta_title', css_class='form-group col-md-6 mb-3'),
                Column('meta_description', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('is_active', css_class='form-group col-md-6 mb-3'),
            ),

            # Submit Button
            Row(
                Column(
                    Submit('submit', 'Save Product', css_class='btn btn-primary btn-lg'),
                    css_class='form-group col-md-12 text-center'
                ),
            )
        )


class ProductFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('brand', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


# dynamic products attibutes form
class ProductAttributeForm(forms.Form):
    attribute = forms.ModelChoiceField(
        queryset=Attribute.objects.all(),
        widget=AttributeWidget(
            attrs={
                'data-minimum-input-length': 0,
            }
        )
    )
    values = forms.ModelMultipleChoiceField(
        queryset=AttributeValue.objects.all(),
        widget=AttributeValueWidget(
            attrs={
                'data-minimum-input-length': 0,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy forms layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('attribute', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('values', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('product', 'image', 'alt_text', 'is_featured')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('product', 'image', 'alt_text', 'is_featured'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class ProductImageFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class ProductImageDirectForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image', 'alt_text', 'is_featured')  # Exclude 'product' field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='form-group col-md-6 mb-0'),
                Column('alt_text', css_class='form-group col-md-6 mb-0'),
                Column('is_featured', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    Submit('submit', 'Upload Image', css_class='btn btn-primary')
                ),
            )
        )


# class ProductVariantForm(forms.ModelForm):
#     attributes = forms.ModelMultipleChoiceField(
#         queryset=AttributeValue.objects.all(),
#         widget=AttributeValueWidget(
#             attrs={
#                 'data-minimum-input-length': 0,
#             }
#         )
#     )

#     initial_stock_quantity = forms.IntegerField(
#         required=False,
#         initial=0,
#         label='Initial Stock Quantity',
#         min_value=0,
#         help_text='Enter the initial stock quantity for this product variant.'
#     )

#     class Meta:
#         model = ProductVariant
#         fields = ('product', 'attributes', 'sku', 'upc', 'price', 'retail_price', 'is_active', 'image','offer_price','offer_start_time','offer_end_time')

#         widgets = {
#             'offer_start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
#             'offer_end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         if self.instance and self.instance.pk:
#             self.fields['product'].disabled = True

#             if not self.instance.product.is_variant:
#                 self.fields.pop('attributes')

#             # Disable the stock_quantity field in edit mode
#             self.fields.pop('initial_stock_quantity')

#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('product', css_class='form-group col-md-6 mb-0'),
#                 Column('attributes', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('sku', css_class='form-group col-md-6 mb-0'),
#                 Column('upc', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('price', css_class='form-group col-md-6 mb-0'),
#                 Column('retail_price', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('offer_price', css_class='form-group col-md-4 mb-0'),
#                 Column('offer_start_time', css_class='form-group col-md-3 mb-0'),
#                 Column('offer_end_time', css_class='form-group col-md-3 mb-0'),
#             ),
#             Row(
#                 Column('initial_stock_quantity', css_class='form-group col-md-6 mb-0'),
#                 Column('is_active', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('image', css_class='form-group col-md-12 mb-0'),
#             ),


#             Row(
#                 Column(
#                     Submit('submit', 'Save', css_class='btn btn-primary', onclick="return confirm('Are you sure you want to submit?');")
#                 ),
#             )
#         )

class ProductVariantForm1(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = (
            'product', 'sku', 'upc',
            'price', 'retail_price',
            'offer_price', 'offer_start_time', 'offer_end_time',
            'stock_quantity',          # real field
            'is_active', 'image',
        )
        widgets = {
            
            'offer_start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'offer_end_time'  : DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['product'].disabled = True
            # self.fields['sku'].initial = self.instance.sku
            self.fields['stock_quantity'].label = "Current stock quantity"
        else:
            self.fields['stock_quantity'].label = "Initial stock quantity"
            
            self.fields['stock_quantity'].initial = 0

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('product', css_class='col-md-6')),
            Row(Column('sku', css_class='col-md-6'),
                Column('upc', css_class='col-md-6')),
            Row(Column('price', css_class='col-md-6'),
                Column('retail_price', css_class='col-md-6')),
            Row(Column('offer_price',      css_class='col-md-4'),
                Column('offer_start_time', css_class='col-md-4'),
                Column('offer_end_time',   css_class='col-md-4')),
            Row(Column('stock_quantity', css_class='col-md-12')),
            Row(Column('image', css_class='col-md-12')),
            Row(Column('is_active', css_class='col-md-12')),
            Row(Column(Submit('save', 'Save'), css_class='text-end')),
        )

    # identical save() as above if you also want audit-trail entries


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = (
            'product', 'sku', 'upc',
            'price', 'retail_price',
            'offer_price', 'offer_start_time', 'offer_end_time',
            'stock_quantity',           # <— use the real model field
            'is_active', 'image', 'attributes',
        )
        widgets = {
            'offer_start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'offer_end_time'  : DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # disable product once the variant exists
        if self.instance.pk:
            self.fields['product'].disabled = True
            # show the current on-hand stock
            self.fields['stock_quantity'].initial = self.instance.stock_quantity
            # self.fields['sku'].initial = self.instance.sku
        else:
            self.fields['stock_quantity'].label = 'Initial stock quantity'

        # crispy layout (trimmed for brevity)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('product',      css_class='col-md-6'),
                Column('attributes',   css_class='col-md-6')),
            Row(Column('sku',          css_class='col-md-6'),
                Column('upc',          css_class='col-md-6')),
            Row(Column('price',        css_class='col-md-6'),
                Column('retail_price', css_class='col-md-6')),
            Row(Column('offer_price',      css_class='col-md-4'),
                Column('offer_start_time', css_class='col-md-4'),
                Column('offer_end_time',   css_class='col-md-4')),
            Row(Column('stock_quantity', css_class='col-md-12')),
            Row(Column('image',        css_class='col-md-12')),
            Row(Column('is_active',    css_class='col-md-12')),
            Row(Column(Submit('save', 'Save'), css_class='text-end')),
        )

    def save(self, commit=True):
        """
        Persist the variant and, if the user changed the quantity,
        write the delta to StockEntry so you keep an audit trail.
        """
        old_qty = self.instance.stock_quantity or 0
        instance = super().save(commit=False)
        new_qty = self.cleaned_data['stock_quantity']

        if commit:
            instance.stock_quantity = new_qty
            instance.save()

            delta = new_qty - old_qty
            if delta != 0:
                StockEntry.objects.create(
                    variant=instance,
                    quantity=abs(delta),
                    change_type='adjustment',
                    adjustment_direction='increase' if delta > 0 else 'decrease',
                    notes='Manual stock edit via variant form',
                )
            self.save_m2m()
        return instance


# class ProductVariantForm(forms.ModelForm):
#     initial_stock_quantity = forms.IntegerField(
#         required=False,
#         initial=0,
#         # label='Initial Stock Quantity',
#         min_value=0,
#         # help_text='Enter the initial stock quantity for this product variant.'
#     )

#     class Meta:
#         model = ProductVariant
#         fields = ('product', 'sku', 'upc', 'price', 'retail_price', 'is_active', 'image',
#                   'offer_price', 'offer_start_time', 'offer_end_time', 'attributes')
#         widgets = {
#             'offer_start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
#             'offer_end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()

#         # Only show initial_stock_quantity for new instances
#         if self.instance.pk:
#             if hasattr(self.fields, 'initial_stock_quantity'):
#                 del self.fields['initial_stock_quantity']

#         # Disable product field for existing instances
#         if self.instance.pk:
#             self.fields['product'].disabled = True

#         self.fields['attributes'] = forms.ModelMultipleChoiceField(
#             queryset=AttributeValue.objects.all(),
#             widget=AttributeValueWidget(
#                 attrs={
#                     'data-minimum-input-length': 0,
#                 }
#             ))

#         # Define the layout based on available fields
#         layout_rows = [
#             Row(
#                 Column('product', css_class='form-group col-md-6 mb-0'),
#                 Column('attributes', css_class='form-group col-md-6 mb-0'),
#             )
#         ]

#         layout_rows.extend([
#             Row(
#                 Column('sku', css_class='form-group col-md-6 mb-0'),
#                 Column('upc', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('price', css_class='form-group col-md-6 mb-0'),
#                 Column('retail_price', css_class='form-group col-md-6 mb-0'),
#             ),
#             Row(
#                 Column('offer_price', css_class='form-group col-md-4 mb-0'),
#                 Column('offer_start_time', css_class='form-group col-md-4 mb-0'),
#                 Column('offer_end_time', css_class='form-group col-md-4 mb-0'),
#             ),
#         ])

#         if 'initial_stock_quantity' in self.fields:
#             layout_rows.append(
#                 Row(
#                     Column('initial_stock_quantity', css_class='form-group col-md-12 mb-0'),
#                 )
#             )

#         # Add image field
#         layout_rows.append(
#             Row(
#                 Column('image', css_class='form-group col-md-12 mb-0'),
#             )
#         )

#         # Add is_active field below image
#         layout_rows.append(
#             Row(
#                 Column('is_active', css_class='form-group col-md-12 mb-0'),
#             )
#         )

#         # Add submit button
#         layout_rows.append(
#             Row(
#                 Column(
#                     Submit('submit', 'Save', css_class='btn btn-primary',
#                            onclick="return confirm('Are you sure you want to submit?');")
#                 ),
#             )
#         )

#         self.helper.layout = Layout(*layout_rows)


class ProductVariantFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-4 mb-0'),
                Column('sku', css_class='form-group col-md-4 mb-0'),
                Column('upc', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['variant', 'quantity', 'change_type', 'adjustment_direction', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        change_type = cleaned_data.get('change_type')
        adjustment_direction = cleaned_data.get('adjustment_direction')

        if change_type == 'adjustment' and not adjustment_direction:
            raise forms.ValidationError("Adjustment direction is required when the change type is 'adjustment'.")

        if change_type != 'adjustment' and adjustment_direction:
            cleaned_data['adjustment_direction'] = None  # Ensure it's empty when not needed

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('variant', 'quantity', 'change_type', 'adjustment_direction', 'notes'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class StockEntryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('variant', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class StockEntryByProductForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity')
    change_type = forms.ChoiceField(
        choices=StockEntry.CHANGE_TYPE_CHOICES,
        label='Change Type'
    )
    adjustment_direction = forms.ChoiceField(
        choices=(
            ('increase', 'Increase'),
            ('decrease', 'Decrease'),
        ),
        required=False,
        label='Adjustment Direction'
    )
    notes = forms.CharField(widget=forms.Textarea, required=False, label='Notes')

    def clean(self):
        cleaned_data = super().clean()
        change_type = cleaned_data.get('change_type')
        adjustment_direction = cleaned_data.get('adjustment_direction')

        min_order_quantity = cleaned_data.get('min_order_quantity')
        max_order_quantity = cleaned_data.get('max_order_quantity')

        if min_order_quantity and max_order_quantity:
            if min_order_quantity > max_order_quantity:
                raise forms.ValidationError(
                    "Minimum order quantity cannot be greater than maximum order quantity."
                )

        if change_type == 'adjustment' and not adjustment_direction:
            self.add_error('adjustment_direction',
                           "Adjustment direction is required when the change type is 'adjustment'.")

        if change_type != 'adjustment' and adjustment_direction:
            cleaned_data['adjustment_direction'] = None  # Ensure it's empty when not needed

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('quantity', 'change_type', 'adjustment_direction', 'notes'),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['name', 'description', 'priority', 'attachment']


class SupportTicketMessageForm(forms.ModelForm):
    class Meta:
        model = SupportTicketMessage
        fields = ['message']


class SupportTicketForm(forms.ModelForm):
    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        required=False,
        empty_label="Select an Order",
        label="Order (if applicable)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    category = forms.ChoiceField(
        choices=SupportTicket.TICKET_CATEGORY_CHOICES,
        label="Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SupportTicket
        fields = ['name', 'description', 'category', 'order', 'priority', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe the issue...'}),
        }


class CreateCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code', 'discount_type', 'discount_value', 'maximum_discount_amount',
            'minimum_order_amount', 'expiration_date', 'max_uses', 'is_active'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter coupon code'}),
            'discount_type': forms.Select(attrs={'class': 'form-select'}),
            'discount_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discount value'}),
            'maximum_discount_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter max discount amount'}),
            'minimum_order_amount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter minimum order amount'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_uses': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter max uses'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom label and help text
        self.fields['discount_type'].label = "Discount Type"
        self.fields['discount_value'].label = "Discount Value"
        self.fields['maximum_discount_amount'].label = "Maximum Discount Amount"
        self.fields['minimum_order_amount'].label = "Minimum Order Amount"
        self.fields['expiration_date'].label = "Expiration Date"
        self.fields['max_uses'].label = "Maximum Uses"
        self.fields['is_active'].label = "Is Active"


from .models import SliderImage


class SliderImageForm(forms.ModelForm):
    class Meta:
        model = SliderImage
        fields = ['image', 'alt_text', 'url', 'title', 'subtitle', 'order', 'is_active']
        widgets = {
            'alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alternative text'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link URL'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtitle'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order'}),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 0;'  # Reset any margin
            }),
        }


from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'user', 'shipping_method', 'coupon', 'status', 'subtotal', 'shipping_cost', 'total_discount',
            'total_amount',
            'payment_status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('user', 'shipping_method', 'coupon', 'status', 'subtotal', 'shipping_cost', 'total_discount',
                       'total_amount', 'payment_status', ),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary',
                           onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )


class OrderFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-4 mb-0'),

                Column('shipping_method', css_class='form-group col-md-4 mb-0'),
                Column('coupon', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),

                Column('payment_status', css_class='form-group col-md-4 mb-0'),

                Column(HTML("""<button class='btn btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0'),
            ),
        )


class FlashDealFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-2 mb-0'),

                Column(HTML("""<button class='btn btn-sm btn-lg btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-5 mb-0 mt-4'),
            ),
        )
