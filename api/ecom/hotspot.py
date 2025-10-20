from django.db.models import Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from apps.ecom.models import ProductVariant
from apps.promo.models import Hotspot, HotspotItem


class HotspotItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotItem
        fields = ['id', 'hot_spot', 'product', 'x_coordinate', 'y_coordinate']

    def to_representation(self, instance):
        r = super(HotspotItemSerializer, self).to_representation(instance)
        r['product_id'] = instance.product.id
        r['name'] = instance.product.name
        r['slug'] = instance.product.slug
        r['description'] = instance.product.description
        r['is_variant'] = True if instance.product.is_variant else False
        price = ProductVariant.objects.filter(product=instance.product).aggregate(
            min=Min('retail_price'), max=Max('retail_price')
        )
        if instance.product.is_variant:
            r['price'] = f"{price['min']}-{price['max']}"
        else:
            r['price'] = str(price['min'])
        return r


class HotspotSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Hotspot
        fields = ['id', 'title', 'slug', 'image', 'items']

    def get_items(self, obj):
        queryset = HotspotItem.objects.filter(hot_spot=obj)
        return HotspotItemSerializer(queryset, many=True).data


class HotspotViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    http_method_names = ['get', ]
