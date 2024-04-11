from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField
from datetime import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')

    def __str__(self):
        return self.user.username

class Section(models.Model):
    
    PAGE_CHOICES = (
        ('home', 'Home'), 
        ('about', 'About'),
        ('contact', 'Contact'),
        ('faq', 'FAQ'),
    )
    
    TYPE_CHOICES = (
        ('hero', 'Hero'),
        ('side-image', 'Text with Side Image'),
    )

    page = models.CharField(max_length=20, choices=PAGE_CHOICES, null=True)
    section_type = models.CharField("Type", max_length=20, choices=TYPE_CHOICES, null=True)
    image = models.ImageField(upload_to="section_images", null=True, blank=True)
    title = models.CharField(max_length=50, null=True)
    subtitle = HTMLField(null=True, blank=True)
    button_1_link = models.URLField(null=True, blank=True)
    button_1_text = models.CharField(max_length=10, null=True, blank=True)
    button_2_link = models.URLField(null=True, blank=True)
    button_2_text = models.CharField(max_length=10, null=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', 'position', 'display']

    def __str__(self):
        return self.title