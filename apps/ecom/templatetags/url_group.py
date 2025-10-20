from django import template

register = template.Library()

@register.filter
def in_url_group(url_name, group_name):
    groups = {
        'products': ['product_list', 'product_add', 'product_update', 'product_delete','product_attribute_dynamic_create','product_add_images'],
        'stocks': [
            'stock_product_wise_update',
            'stockentry_delete',
            'stockentry_update',
            'stockentry_add',
            'stockentry_list'
        ],
        'productvariants': [
            'productvariant_delete',
            'productvariant_update',
            'productvariant_add',
            'productvariant_list'
        ],
        'attributes': ['attribute_list', 'attribute_add', 'attribute_update', 'attribute_delete'],
        'attributesvalues':[ 'attributevalue_list', 'attributevalue_add','attributevalue_delete','attributevalue_update'],
        'categories': ['category_list', 'category_add', 'category_update', 'category_delete'],
        'brands': ['brand_list', 'brand_add', 'brand_update', 'brand_delete'],
        'tags': ['tag_list', 'tag_add', 'tag_update', 'tag_delete'],
        'taxes': ['tax_list', 'tax_add', 'tax_update', 'tax_delete'],
        'inventory': ['requisition_list', 'purchase_order_add','create_requisition','edit_requisition','supplier_list','supplier_add','supplier_update','supplier_delete','purchase_order_list','purchase_order_edit','purchase_order_display','purchase_order_create','po_list','po_details_display'],
        'admin_menus': ['group_permission_view','customeruser_list','staffuser_list'],
        'supplier': ['supplier_list','supplier_add','supplier_update','supplier_delete'], 
        'flash_deals': ['flash_deals','flash_deal_create','flash_deal_edit','flash_deals_delete'],
        'settings': ['businesslocation_list','businesslocation_add','businesslocation_update','businesslocation_delete']
    }
    return url_name in groups.get(group_name, [])


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()