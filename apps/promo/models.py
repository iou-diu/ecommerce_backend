import random
import string

from django.db import models
from django.utils.text import slugify

from apps.ecom.models import Product


# Create your models here.
class Hotspot(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        # Automatically generate slug if not already provided
        if not self.slug:
            slug_base = slugify(self.title)
            unique_suffix = ''.join(random.choices(string.digits, k=4))  # Generate a 4-digit random number
            self.slug = f"{slug_base}-{unique_suffix}"
        super().save(*args, **kwargs)  # Call the parent save method


class HotspotItem(models.Model):
    hot_spot = models.ForeignKey(Hotspot, on_delete=models.CASCADE, related_name='hot_spot_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='hot_spot_product')
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
