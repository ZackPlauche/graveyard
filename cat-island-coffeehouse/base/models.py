from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')

    def __str__(self):
        return self.user.username

class ExploreSection(models.Model):
    image = models.ImageField(upload_to="images", null=True)
    title = models.CharField(max_length=20, null=True)
    body = models.TextField(null=True)
    button_link = models.URLField(null=True, blank=True)
    button_text = models.CharField(max_length=15, null=True, blank=True)
    display = models.BooleanField(default=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    IMAGE_POSITIONS = [
        ('auto','Auto'),
        ('left','Left'),
        ('right','Right')
    ]
    image_position = models.CharField(max_length=5, choices=IMAGE_POSITIONS, default='auto')

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return slugify(self.title)

class Testimonial(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    profile_image = models.ImageField(upload_to="images", help_text="Image must be formatted to a 1:1 ratio (square image).")
    review = models.TextField(null=True)
    display = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_name_initial(self):
        return f"{self.first_name} {self.last_name[0]}."

    def __str__(self):
        return self.full_name
    
    
    
