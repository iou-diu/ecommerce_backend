import django_tables2 as tables
from django.utils.html import format_html
from urllib.parse import urlencode
from apps.helpers import CustomTable
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from .models import Address, Attribute, AttributeValue, Brand, Category, Coupon, FlashDeal, Order, Product, ProductImage, ProductVariant, SliderImage, StockEntry, SupportTicket, Tag, Tax

class CategoryTable(CustomTable):
    
    edit_url = 'category_update'
    delete_url = 'category_delete'
    class Meta:
        model = Category
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'parent', 'image', 'description', 'meta_title', 'meta_description', 'slug', 'is_featured', 'for_product', 'for_solution', 'is_active')
        empty_text = 'No categorys available'
        orderable = True
        exclude = ('selected',)


class AddressTable(CustomTable):
    edit_url = 'address_update'
    delete_url = 'address_delete'
    class Meta:
        model = Address
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['user', 'full_name', 'address_line_1', 'address_line_2', 'city', 'state_or_province', 'postal_code', 'country', 'phone_number', 'is_default_shipping', 'is_default_billing']
        empty_text = 'No addresss available'
        orderable = True
        exclude = ('selected',)


class BrandTable(CustomTable):
    edit_url = 'brand_update'
    delete_url = 'brand_delete'
    class Meta:
        model = Brand
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'logo', 'description', 'meta_title', 'meta_description', 'slug', 'is_active']
        empty_text = 'No brands available'
        orderable = True
        exclude = ('selected',)


class AttributeTable(CustomTable):
    edit_url = 'attribute_update'
    delete_url = 'attribute_delete'
    class Meta:
        model = Attribute
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'data_type', 'unit', 'is_filterable', 'is_variation']
        empty_text = 'No attributes available'
        orderable = True
        exclude = ('selected',)


class AttributeValueTable(CustomTable):
    edit_url = 'attributevalue_update'
    delete_url = 'attributevalue_delete'

    color = tables.Column(empty_values=(), verbose_name='Color Code', orderable=False,attrs={"td": {"width": "170"}})

    def render_color(self, record):
        if record.color_code:
            return format_html(
                '''
                <div class="row align-items-center">
                    <div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>
                    <span class="mx-2"> {}</span>
                    <button class="btn btn-sm btn-outline-secondary" onclick="copyToClipboard('{}')">Copy</button>
                </div>
                ''',
                record.color_code,  # First placeholder for the background color
                record.color_code,  # Second placeholder for displaying the color code
                record.color_code   # Third placeholder for the color code to be copied
            )

        return mark_safe("")


    class Meta:
        model = AttributeValue
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['attribute', 'value','color']
        empty_text = 'No attributevalues available'
        orderable = True
        exclude = ('selected',)


class TagTable(CustomTable):
    edit_url = 'tag_update'
    delete_url = 'tag_delete'
    class Meta:
        model = Tag
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name']
        empty_text = 'No tags available'
        orderable = True
        exclude = ('selected',)


class TaxTable(CustomTable):
    edit_url = 'tax_update'
    delete_url = 'tax_delete'
    class Meta:
        model = Tax
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'value','tax_type', 'is_active']
        empty_text = 'No taxs available'
        orderable = True
        exclude = ('selected',)


class ProductTable(CustomTable):
    edit_url = 'product_update'
    delete_url = 'product_delete'
    attributes = tables.Column(empty_values=(), verbose_name='Set Properties', orderable=False,attrs={"td": {"width": "170"}})

    def render_attributes(self, record):
        attributes_url = reverse_lazy('product_attribute_dynamic_create', kwargs={'product_id':  record.pk})
        images_url = reverse_lazy('product_add_images', kwargs={'product_id':  record.pk})
        stockvariant_url = f"{reverse_lazy('productvariant_list')}?{urlencode({'product': record.pk})}"

        # Determine the button text and color based on whether it's a variant
        if record.is_variant:
            stock_button_text = "Stock Variants"
            stock_button_class = "btn-success"  # Green button for variants
        else:
            stock_button_text = "Default Stock"
            stock_button_class = "btn-danger"  # Red button for default stock

        # Create the formatted stock variant URL with the dynamic class and text
        formatted_stockvariant_url = '''<a href="%s" class="btn btn-sm %s mt-2 btn-block"><i class="fa fa-th-list" aria-hidden="true"></i> %s</a>''' % (stockvariant_url, stock_button_class, stock_button_text)

        # Concatenate the URLs for attributes, images, and stock variant
        url = '''<a href="%s" class="btn btn-sm btn-info btn-block"><i class="fa fa-list-ul"></i> Set Attributes</a>''' % attributes_url
        url += '''<a href="%s" class="btn btn-sm btn-primary mt-2 btn-block"><i class="fa fa-file-image" aria-hidden="true"></i> Set Images</a>''' % images_url
        url += formatted_stockvariant_url

        return mark_safe(url)

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'category', 'brand',  'slug', 'is_active', 'created_at', 'attributes'
        ]
        empty_text = 'No products available'
        orderable = True
        exclude = ('selected',)


class ProductImageTable(CustomTable):
    edit_url = 'productimage_update'
    delete_url = 'productimage_delete'
    class Meta:
        model = ProductImage
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['product', 'image', 'alt_text', 'is_featured', 'uploaded_at']
        empty_text = 'No productimages available'
        orderable = True
        exclude = ('selected',)


class ProductVariantTable(CustomTable):
    edit_url = 'productvariant_update'
    delete_url = 'productvariant_delete'

    stock_management = tables.Column(empty_values=(), verbose_name='Stock Management', orderable=False,attrs={"td": {"width": "150"}})


    def render_stock_management(self, record):
        stock_update_url = reverse_lazy('stock_product_wise_update', kwargs={'variant_id':  record.pk})
      
    
        url = '''<a href="%s" class="btn btn-sm btn-info btn-block"><i class="fa fa-th-list"></i> Update Stock</a>''' % stock_update_url
       
        return mark_safe(url)

    class Meta:
        model = ProductVariant
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['product', 'sku', 'upc', 'price', 'retail_price', 'is_active', 'image', 'stock_quantity','stock_management'
        ]
        empty_text = 'No productvariants available'
        orderable = True
        exclude = ('selected',)


class StockEntryTable(CustomTable):
    edit_url = 'stockentry_update'
    delete_url = 'stockentry_delete'
    quantity = tables.Column(verbose_name='Quantity')

    def render_quantity(self, value, record):
        signed_quantity = record.get_signed_quantity()
        return f"{signed_quantity:+d}"  # Displays '+' or '-' sign
    
    class Meta:
        model = StockEntry
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['variant', 'quantity', 'change_type', 'timestamp', 'notes']
        empty_text = 'No stockentrys available'
        orderable = True
        exclude = ('selected',)

class SupportTicketTable(CustomTable):
    # Define actions like View, Assign, Close Ticket within the table
    actions = tables.Column(empty_values=(), orderable=False)

    def render_actions(self, record):
        view_url = reverse_lazy('ticket_detail', kwargs={'ticket_id': record.ticket_id})
        # assign_url = reverse_lazy('support_ticket_assign', kwargs={'ticket_id': record.ticket_id})
        # close_url = reverse_lazy('support_ticket_close', kwargs={'ticket_id': record.ticket_id})

        return format_html(
            '''
            <a href="{}" class="btn btn-sm btn-primary">View</a>
          
            ''',
            view_url
        )

    class Meta:
        model = SupportTicket
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['ticket_id', 'name', 'status', 'priority', 'created_at']
        empty_text = 'No support tickets available'
        orderable = True


class CouponTable(tables.Table):
    class Meta:
        model = Coupon
        template_name = 'django_tables2/bootstrap4.html'  # or any other template style you prefer
        fields = [
            'code', 'discount_type', 'discount_value', 'maximum_discount_amount',
            'minimum_order_amount', 'expiration_date', 'max_uses', 'is_active'
        ]
        attrs = {"class": "table table-bordered table-striped"}
class SliderImageTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False)

    def render_actions(self, record):
        edit_url = reverse_lazy('slider_image_update', kwargs={'pk': record.pk})
        delete_url = reverse_lazy('slider_image_delete', kwargs={'pk': record.pk})

        # Inline delete form without embedding CSRF token directly here
        return format_html(
            '''
            <a href="{}" class="btn btn-sm btn-primary">Edit</a>
            <form action="{}" method="post" style="display:inline;" class="delete-form">
                <button type="submit" class="btn btn-sm btn-danger">Delete</button>
            </form>
            ''',
            edit_url, delete_url
        )

    class Meta:
        model = SliderImage
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['image', 'alt_text', 'url', 'title', 'subtitle', 'order', 'is_active', 'created_at']


class OrderTable(CustomTable):
    edit_url = 'order_update'
    delete_url = 'order_delete'

    # Add actions column to show view icon and modal functionality
    actions = tables.Column(empty_values=(), orderable=False, attrs={"td": {"width": "140"}})

    def render_actions(self, record):
        # compute absolute URLs server-side to avoid relative-path duplication
        detail_url = reverse_lazy('order_detail_json', kwargs={'pk': record.pk})
        update_url = reverse_lazy('order_update_status', kwargs={'pk': record.pk})

        tpl = '''
            <button class="btn btn-sm btn-outline-primary order-view-btn"
                    data-order-id="{ID_PLACEHOLDER}"
                    data-detail-url="{DETAIL_URL}"
                    data-update-url="{UPDATE_URL}"
                    title="View Order">
                <i class="fa fa-eye"></i>
            </button>

            <script>
            (function () {
                if (window.__orderModalInitialized) return;
                window.__orderModalInitialized = true;

                function ensureModal() {
                    if (document.getElementById('orderDetailModal')) return;
                    var modalHtml = '<div class="modal fade" id="orderDetailModal" tabindex="-1" role="dialog">' +
                        '<div class="modal-dialog modal-lg" role="document"><div class="modal-content">' +
                        '<div class="modal-header"><h5 class="modal-title">Order Details</h5>' +
                        '<button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span></button></div>' +
                        '<div class="modal-body"><div id="orderDetailContent">Loading...</div></div>' +
                        '<div class="modal-footer"><div class="mr-auto" id="orderStatusControls"></div>' +
                        '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>' +
                        '<button id="saveOrderStatusBtn" class="btn btn-primary">Save Status</button>' +
                        '</div></div></div></div>';
                    var div = document.createElement('div');
                    div.innerHTML = modalHtml;
                    document.body.appendChild(div);
                }

                function escapeHtml(s) {
                    if (s === null || s === undefined) return '';
                    return String(s);
                }

                function loadOrderDetails(detailUrl) {
                    var content = document.getElementById('orderDetailContent');
                    var statusControls = document.getElementById('orderStatusControls');
                    content.innerHTML = 'Loading...';
                    statusControls.innerHTML = '';

                    return fetch(detailUrl, {
                        credentials: 'same-origin',
                        headers: { 'Accept': 'application/json' }
                    })
                    .then(function (resp) {
                        if (!resp.ok) throw new Error('Failed to fetch order details');
                        return resp.json();
                    })
                    .then(function (data) {
                        var html = '<div class="row">';
                        html += '<div class="col-md-6"><h6>Order</h6><ul class="list-unstyled">';
                        html += '<li><strong>ID:</strong> ' + escapeHtml(data.id) + '</li>';
                        html += '<li><strong>User:</strong> ' + escapeHtml(data.user || '-') + '</li>';
                        html += '<li><strong>Created:</strong> ' + escapeHtml(data.created_at) + '</li>';
                        html += '<li><strong>Status:</strong> ' + escapeHtml(data.status) + '</li>';
                        html += '<li><strong>Payment:</strong> ' + escapeHtml(data.payment_status) + '</li>';
                        html += '</ul></div>';

                        html += '<div class="col-md-6"><h6>Amounts</h6><ul class="list-unstyled">';
                        html += '<li><strong>Subtotal:</strong> ' + escapeHtml(data.subtotal) + '</li>';
                        html += '<li><strong>Shipping:</strong> ' + escapeHtml(data.shipping_cost) + '</li>';
                        html += '<li><strong>Total Discount:</strong> ' + escapeHtml(data.total_discount) + '</li>';
                        html += '<li><strong>Total Amount:</strong> ' + escapeHtml(data.total_amount) + '</li>';
                        html += '</ul></div></div>';

                        html += '<hr/><h6>Shipping Address</h6>';
                        if (data.shipping_address) {
                            html += '<div>' + escapeHtml(data.shipping_address.display) + '</div>';
                        } else {
                            html += '<div>-</div>';
                        }

                        html += '<hr/><h6>Billing Address</h6>';
                        if (data.billing_address) {
                            html += '<div>' + escapeHtml(data.billing_address.display) + '</div>';
                        } else {
                            html += '<div>-</div>';
                        }

                        html += '<hr/><h6>Items</h6>';
                        html += '<table class="table table-sm table-bordered"><thead><tr><th>Product</th><th>SKU</th><th>Qty</th><th>Unit</th><th>Total</th></tr></thead><tbody>';
                        (data.order_lines || []).forEach(function (line) {
                            html += '<tr>';
                            html += '<td>' + escapeHtml(line.product_name) + '</td>';
                            html += '<td>' + escapeHtml(line.sku) + '</td>';
                            html += '<td>' + escapeHtml(line.quantity) + '</td>';
                            html += '<td>' + escapeHtml(line.final_price) + '</td>';
                            html += '<td>' + escapeHtml(line.total_price) + '</td>';
                            html += '</tr>';
                        });
                        html += '</tbody></table>';

                        if (data.notes) {
                            html += '<hr/><h6>Notes</h6><div>' + escapeHtml(data.notes) + '</div>';
                        }

                        content.innerHTML = html;

                        // status / payment controls
                        var statusOptions = data.available_statuses || [];
                        var paymentOptions = data.available_payment_statuses || [];
                        var statusHtml = '<label>Order Status</label><select id="modal_order_status" class="form-control">';
                        statusOptions.forEach(function (s) {
                            var sel = s[0] === data.status ? 'selected' : '';
                            statusHtml += '<option value="' + s[0] + '" ' + sel + '>' + s[1] + '</option>';
                        });
                        statusHtml += '</select>';

                        statusHtml += '<label class="mt-2">Payment Status</label><select id="modal_payment_status" class="form-control">';
                        paymentOptions.forEach(function (s) {
                            var sel = s[0] === data.payment_status ? 'selected' : '';
                            statusHtml += '<option value="' + s[0] + '" ' + sel + '>' + s[1] + '</option>';
                        });
                        statusHtml += '</select>';

                        statusHtml += '<label class="mt-2">Notes</label><textarea id="modal_order_notes" class="form-control" rows="2">' + (data.notes ? data.notes : '') + '</textarea>';
                        statusControls.innerHTML = statusHtml;

                        return data;
                    });
                }

                // Delegated click handler for any .order-view-btn
                document.body.addEventListener('click', function (e) {
                    var btn = e.target.closest && e.target.closest('.order-view-btn');
                    if (!btn) return;
                    var detailUrl = btn.getAttribute('data-detail-url');
                    var updateUrl = btn.getAttribute('data-update-url');
                    if (!detailUrl) return;

                    ensureModal();

                    loadOrderDetails(detailUrl)
                    .then(function (data) {
                        // attach save handler (use the updateUrl read from the button)
                        var saveBtn = document.getElementById('saveOrderStatusBtn');
                        saveBtn.onclick = function () {
                            var payload = {
                                status: document.getElementById('modal_order_status').value,
                                payment_status: document.getElementById('modal_payment_status').value,
                                notes: document.getElementById('modal_order_notes').value
                            };
                            if (!updateUrl) {
                                alert('Update URL not available.');
                                return;
                            }
                            fetch(updateUrl, {
                                method: 'POST',
                                credentials: 'same-origin',
                                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                                body: JSON.stringify(payload)
                            })
                            .then(function (resp) { if (!resp.ok) throw new Error('Failed to update order'); return resp.json(); })
                            .then(function (r) {
                                // update table row cells for this order and close modal
                                try {
                                    var tr = btn.closest('tr');
                                    if (tr) {
                                        var table = tr.closest('table');
                                        var headers = Array.from(table.querySelectorAll('thead th')).map(function(h){ return h.textContent.trim().toLowerCase(); });
                                        var cells = tr.querySelectorAll('td');

                                        // find index for order status (exclude payment) and payment status
                                        var statusIndex = headers.findIndex(function(h){ return h.includes('status') && !h.includes('payment'); });
                                        var paymentIndex = headers.findIndex(function(h){ return h.includes('payment'); });

                                        if (statusIndex !== -1 && cells[statusIndex]) {
                                            cells[statusIndex].textContent = r.status || '';
                                        }
                                        if (paymentIndex !== -1 && cells[paymentIndex]) {
                                            cells[paymentIndex].textContent = r.payment_status || '';
                                        }
                                    }
                                } catch (err) {
                                    console.warn('Failed to update table row:', err);
                                }

                                // close modal
                                var modalElem = document.getElementById('orderDetailModal');
                                if (window.jQuery && jQuery(modalElem).modal) {
                                    jQuery(modalElem).modal('hide');
                                } else if (window.bootstrap && bootstrap.Modal) {
                                    var inst = bootstrap.Modal.getInstance(modalElem) || new bootstrap.Modal(modalElem);
                                    inst.hide();
                                } else {
                                    modalElem.style.display = 'none';
                                }

                                // optional small notification
                                try { if (window.toastr) toastr.success('Order updated'); else console.log('Order updated'); } catch(e){}

                            })
                            .catch(function (err) {
                                alert('Error updating order: ' + err.message);
                            });
                        };

                        // show modal: support Bootstrap 4 (jQuery) and Bootstrap 5 (vanilla)
                        var modalElem = document.getElementById('orderDetailModal');
                        if (window.jQuery && jQuery(modalElem).modal) {
                            jQuery(modalElem).modal('show');
                        } else if (window.bootstrap && bootstrap.Modal) {
                            var m = new bootstrap.Modal(modalElem);
                            m.show();
                        } else {
                            modalElem.style.display = 'block';
                        }
                    })
                    .catch(function (err) {
                        var content = document.getElementById('orderDetailContent');
                        content.innerHTML = '<div class="alert alert-danger">Error loading order details</div>';
                        console.error(err);
                    });
                });
            })();
            </script>
        '''
        # inject server-side resolved URLs (escape them safely)
        return mark_safe(
            tpl.replace('{ID_PLACEHOLDER}', str(record.pk))
               .replace('{DETAIL_URL}', str(detail_url))
               .replace('{UPDATE_URL}', str(update_url))
        )

    class Meta:
        model = Order
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['user',  'shipping_method', 'coupon', 'status', 'subtotal', 'shipping_cost', 'total_discount', 'total_amount', 'payment_status', 'created_at', 'actions']
        empty_text = 'No orders available'
        orderable = True
        exclude = ('selected',)


# Keep FlashDealTable: used by FlashDealList/FlashDealView and referenced in views.py.
# Do not remove — the FlashDealListView / FlashDealView depend on this table class.
class FlashDealTable(CustomTable):
    edit_url = 'tag_update'
    delete_url = 'tag_delete'
    class Meta:
        model = FlashDeal
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['title','start_date','end_date','is_active']
        empty_text = 'No tags available'
        orderable = True
        exclude = ('selected',)
