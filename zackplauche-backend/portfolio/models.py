from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from .choices import ProjectStatus, OfferType, PricingModel, RequestStatus

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    site_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    
    # Controllers
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=ProjectStatus.choices, blank=True)

    # Relationships
    thumbnail = models.ForeignKey('portfolio.Image', on_delete=models.SET_NULL, blank=True, null=True)
    technologies = models.ManyToManyField('portfolio.Technology', help_text='Technologies used for this project.', blank=True, related_name='projects')

    def __str__(self):
        return self.title


class Image(models.Model):
    """
    General purpose image model.
    """
    alt = models.CharField('alt / title', max_length=255)
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.alt if self.alt else str(self.id)


class File(models.Model):
    """
    General purpose file class to deliver documents, ebooks, etc. to site visitors.
    """
    file = models.FileField(upload_to='files/', blank=True, null=True)
    url = models.URLField(blank=True)


class Technology(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ForeignKey('portfolio.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='technologies')

    class Meta:
        verbose_name_plural = 'technologies'

    def __str__(self):
        return self.title


class Offer(models.Model):
    """
    A general offer model to take care of any and all offer requests.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sales_copy = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=OfferType.choices, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    pricing_model = models.CharField(max_length=255, choices=PricingModel.choices, default=PricingModel.CUSTOM)
    action_url = models.URLField(help_text='The url you want the offer to go to after being clicked on.', blank=True, null=True)
    call_to_action = models.CharField(max_length=255, blank=True, null=True)

    # Controllers
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    experimental = models.BooleanField(default=False)
    show_pricing = models.BooleanField(default=False)

    # Relationships
    category = models.ForeignKey('portfolio.OfferCategory', related_name='offers', on_delete=models.SET_NULL, blank=True, null=True)
    icon = models.ForeignKey('portfolio.Image', related_name='offers_using_as_icon', on_delete=models.SET_NULL, blank=True, null=True)
    thumbnail = models.ForeignKey('portfolio.Image', related_name='offers_using_as_thumbnail', on_delete=models.SET_NULL, blank=True, null=True)
    included = models.ManyToManyField('self', blank=True)
    file = models.ForeignKey('portfolio.File', related_name='offers', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class OfferCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class OfferRequest(models.Model):
    details = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    # Controllers
    status = models.CharField(max_length=255, choices=RequestStatus.choices, default=RequestStatus.NEW)

    offer = models.ForeignKey("portfolio.Offer", related_name='requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='offer_requests', on_delete=models.CASCADE)


class Review(models.Model):
    """
    A general client review that may or may not be associated to a certain offer and client.
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    client_first_name = models.CharField(max_length=255, null=True)
    client_last_name = models.CharField(max_length=255, null=True)
    client_role = models.CharField(max_length=255, blank=True)
    client_company = models.CharField(max_length=255, blank=True)
    date_written = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=255, blank=True, null=True)

    # Controllers
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    # Relationships
    client_image = models.ForeignKey('portfolio.Image', on_delete=models.SET_NULL, null=True, blank=True)
    offer = models.ForeignKey('portfolio.Offer', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.client_first_name} {self.client_last_name}\'s Review'

