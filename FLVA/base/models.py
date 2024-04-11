from django.db import models
from django.utils.text import slugify
from datetime import date

# Create your models here.
class Post(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    title = models.CharField(max_length=100, null=True, unique=True)
    body = models.TextField(null=True)
    display = models.BooleanField(default=False)
    pub_date = models.DateField()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def contains_image(self):
        return bool(self.image)

class Contact(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True, blank=True)

    def full_name(self):
        return f'{first_name} {last_name}'

    def __str__(self):
        return self.email

class FAQ(models.Model):
    question = models.CharField(max_length=200, null=True, help_text="Max Characters: 200", unique=True)
    answer = models.TextField(max_length=200, null=True, blank=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class AboutSection(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    body = models.TextField(null=True)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.title

class Event(models.Model):
    image = models.ImageField(upload_to="images", null=True)
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True)
    EVENT_TYPE_CHOICES = (
        ('In Person', 'In Person', ),
        ('Online', 'Online')
    )
    type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, null=True, default="Online")
    location = models.URLField(null=True, blank=True, help_text="Enter the link to the location of the event.")
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def contains_image(self):
        return bool(self.image)

    def has_passed(self):
        return date.today() > self.date


    @property
    def slug(self):
        return slugify(self.title)
