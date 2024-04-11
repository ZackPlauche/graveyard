from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Restaurant(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    credit_name = models.CharField(max_length=255)
    credit_value = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurants_created')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='restaurants_owned')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='restaurants_managed', blank=True)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='restaurants_staffed', blank=True)
    
    def __str__(self):
        return self.title

    def clean(self):
        self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Tier(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.00'))
    active = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    features = models.JSONField(default=list)

    restaurant = models.ForeignKey('catering.Restaurant', on_delete=models.CASCADE, related_name='tiers')

    def __str__(self):
        return self.title


class Menu(models.Model):
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, editable=False, null=True)

    restaurant = models.ForeignKey('catering.Restaurant', on_delete=models.CASCADE, blank=True, null=True, related_name='menus')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.00'))

    menu = models.ForeignKey('catering.Menu', on_delete=models.SET_NULL, null=True, related_name='items')
    
    def __str__(self):
        return self.title
    

class Ingredient(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    special_instructions = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
