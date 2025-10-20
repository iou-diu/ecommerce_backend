from django.contrib import admin

from .models import Solution


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories', 'created_at', 'updated_at')
    search_fields = ('title', 'overview', 'short_description')
    list_filter = ('categories', 'created_at')
    ordering = ('-created_at',)

    # Optional: display JSON nicely in admin
    readonly_fields = ('formatted_key_features', 'formatted_technical_features', 'formatted_images')

    def formatted_key_features(self, obj):
        return ", ".join(obj.key_features) if isinstance(obj.key_features, list) else str(obj.key_features)

    formatted_key_features.short_description = "Key Features"

    def formatted_technical_features(self, obj):
        return ", ".join([f"{k}: {v}" for k, v in obj.technical_features.items()]) if isinstance(obj.technical_features,
                                                                                                 dict) else str(
            obj.technical_features)

    formatted_technical_features.short_description = "Technical Features"

    def formatted_images(self, obj):
        return ", ".join(obj.images) if isinstance(obj.images, list) else str(obj.images)

    formatted_images.short_description = "Images"
