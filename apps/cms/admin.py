from django.contrib import admin

from apps.cms.models import HomeSlider, Gallery, Brochure, NewsPress


# Register your models here.
@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'order')
    search_fields = ('title', 'type')
    ordering = ('order',)
    list_filter = ('type',)

    fieldsets = (
        (None, {
            'fields': ('title', 'type', 'description', 'image', 'button_title', 'button_link', 'order')
        }),
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('type', 'is_featured')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': (
                'title', 'type', 'location', 'description', 'image', 'video', 'embed_url', 'audio', 'is_featured')
        }),
    )


@admin.register(Brochure)
class BrochureAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'is_file', 'file', 'link', 'description')
        }),
    )


@admin.register(NewsPress)
class NewsPressAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'is_featured')
    search_fields = ('title', 'description')
    list_filter = ('is_featured',)
    # summernote_fields = ('body',)
    """Admin interface for NewsPress model."""
    fieldsets = (
        (None, {
            'fields': (
                'user', 'title', 'slug', 'release_link', 'thumbnail', 'banner', 'short_description', 'body', 'status',
                'is_published', 'is_featured', 'published_date', 'meta_description')
        }),
    )
