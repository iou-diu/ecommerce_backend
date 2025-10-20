from django.db import models

from django.utils.text import slugify

from apps.ecom.models import Category


# Create your models here.
class Solution(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=355, unique=True, blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='solutions')
    overview = models.TextField()
    short_description = models.TextField()
    key_features = models.JSONField(default=dict)
    technical_features = models.JSONField(default=dict)
    thumbnail = models.ImageField(upload_to='solutions/thumbnails/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    images = models.JSONField(default=list)  # List of image URLs or paths

    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    faqs = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"
        ordering = ['-created_at']  # Order by creation date, newest first

    # def category_name(self):
    #     return self.categories.name if self.categories else "No Category"
