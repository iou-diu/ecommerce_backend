from django.db import models
from apps.user.models import CustomUser


# Create your models here.
class HomeSlider(models.Model):
    type = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='home_slider/', blank=True, null=True)
    button_title = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or 'Home Slider Item'


class Gallery(models.Model):
    """Model to represent a gallery item."""

    class Types(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'

    type = models.CharField(max_length=10, choices=Types.choices, default=Types.IMAGE)
    title = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='gallery/audios/', blank=True, null=True)
    embed_url = models.URLField(blank=True, null=True, help_text="For embedding videos or audio from external sources.")
    created_at = models.DateTimeField(auto_now_add=True)

    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'

    def __str__(self):
        return self.title or 'Gallery Item'

    def get_file(self):
        """Returns the appropriate file based on the type."""
        if self.type == self.Types.IMAGE:
            return self.image
        elif self.type == self.Types.VIDEO:
            return self.video
        elif self.type == self.Types.AUDIO:
            return self.audio
        return None


class Brochure(models.Model):
    """Model to represent a brochure item."""
    title = models.CharField(max_length=100, blank=True, null=True)
    is_file = models.BooleanField(default=True, help_text="Check if the brochure is uploaded as a file.")
    file = models.FileField(upload_to='brochures/', blank=True, null=True)
    link = models.URLField(blank=True, null=True, help_text="Link to the brochure if not uploaded as a file.")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Brochure'
        verbose_name_plural = 'Brochures'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_file:
            if not self.file:
                raise ValidationError("File must be provided if 'is_file' is checked.")
        else:
            if not self.link:
                raise ValidationError("Link must be provided if 'is_file' is not checked.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or 'Brochure Item'


class NewsPress(models.Model):
    """Model to represent a news press item."""
    TYPE_CHOICES = [
        (1, 'News'),
        (2, 'Press Release'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_article')
    title = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=500)
    thumbnail = models.ImageField(upload_to='article_thumb', null=True, blank=True)
    banner = models.ImageField(upload_to='article_banner', null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    status = models.PositiveIntegerField(choices=TYPE_CHOICES, default=1)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    no_of_view = models.IntegerField(default=0)
    release_link = models.URLField(blank=True, null=True, help_text="Link to the full news or press release.")
    meta_description = models.TextField(null=True, blank=True)


class ContactForm(models.Model):
    """Model to represent a contact form submission."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Form'
        verbose_name_plural = 'Contact Forms'

    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"
