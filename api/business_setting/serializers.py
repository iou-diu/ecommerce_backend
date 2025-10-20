# serializers.py
from rest_framework import serializers

from api.ecom.hotspot import HotspotSerializer
from apps.ecom.models import BusinessSetting, Category
from apps.promo.models import Hotspot


class SettingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image']


class BusinessSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSetting
        fields = ['key', 'value', 'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.key == 'inspiration_collection' or instance.key == 'unique_collection' or instance.key == 'menu_categories':
            # Ensure value is a list of integers
            ids = instance.value
            if isinstance(ids, str):
                ids = [int(i) for i in ids.split(',') if i.isdigit()]  # Convert to a list of integers

            cats = Category.objects.filter(id__in=ids).distinct()
            representation['categories'] = SettingCategorySerializer(cats, many=True).data
        if instance.key == 'home_banner_settings':
            try:
                representation['title'] = instance.value['title']  # Changed from .title to ['title']
                hotspot = Hotspot.objects.get(
                    id=instance.value['gallery_id'])  # Changed from .gallery_id to ['gallery_id']
                representation['hotspot'] = HotspotSerializer(hotspot).data
            except (KeyError, Hotspot.DoesNotExist, AttributeError) as e:
                representation['title'] = ''
                representation['hotspot'] = {}

        return representation
