from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email Address')
    username = None  # We will use email as the username
    name = models.CharField(max_length=150, verbose_name='Full Name')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related_name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Custom related_name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()  # Use the custom manager

    def __str__(self):
        return f"{self.name} ({self.email})"


class Otp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.user.email}) - {self.otp}"


# The rest of your code stays the same
class AdminUser(CustomUser):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def save(self, *args, **kwargs):
        self.is_superuser = True
        self.is_staff = True
        super().save(*args, **kwargs)
        group, _ = Group.objects.get_or_create(name='Admin')
        self.groups.set([group])


class StaffUser(CustomUser):
    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff Members'

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)
        group, _ = Group.objects.get_or_create(name='Staff')
        self.groups.set([group])


class CustomerUser(CustomUser):
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, _ = Group.objects.get_or_create(name='Customer')
        self.groups.set([group])
