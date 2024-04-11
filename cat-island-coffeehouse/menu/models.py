from django.db import models
from django.utils.text import slugify

# Create your models here.

class MenuCategory(models.Model):
    name = models.CharField(max_length=20, null=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    order = models.PositiveIntegerField(null=True)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'display', 'name']
        verbose_name_plural = 'Menu categories'


    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=40, null=True, unique=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True,
                              help_text="Enter the price in 0.00 format. Will be shown in USD.")
    display = models.BooleanField(default=True)
    favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']
        verbose_name = 'Menu item'

    @property
    def slug(self):
        return slugify(self.title)

    def __str__(self):
        return self.title
