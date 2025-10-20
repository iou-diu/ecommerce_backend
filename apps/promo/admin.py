from django.contrib import admin

from apps.promo.models import Hotspot, HotspotItem


# Register your models here.
class HotspotItemInline(admin.TabularInline):
    model = HotspotItem
    extra = 1  # Number of empty forms to display


@admin.register(Hotspot)
class HotspotAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')  # Customize the displayed fields
    search_fields = ('title',)  # Add a search box for the title
    inlines = [HotspotItemInline]  # Add the TabularInline for HotspotItem
