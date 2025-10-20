from rest_framework import serializers
from apps.cms.models import HomeSlider, Gallery, Brochure, NewsPress, ContactForm
from apps.solutions.models import Solution


class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class BrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = '__all__'


class NewsPressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPress
        fields = ['id', 'title', 'slug', 'thumbnail', 'banner', 'short_description', 'is_featured', 'release_link',
                  'published_date']
        read_only_fields = ('user', 'slug', 'published_date')


class NewsPressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPress
        fields = '__all__'
        read_only_fields = ('user', 'slug', 'published_date')


class SolutionListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='categories.name', read_only=True)

    class Meta:
        model = Solution
        fields = ['id', 'title', 'slug', 'category_name', 'thumbnail', 'short_description', 'created_at']


class SolutionDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='categories.name', read_only=True)

    class Meta:
        model = Solution
        fields = '__all__'


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'
        read_only_fields = ['created_at']
