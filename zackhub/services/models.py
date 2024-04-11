from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from .choices import PricingModel


class Service(Page):
    icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    description = RichTextField(blank=True, features=['bold', 'italic', 'ul', 'ol', 'link', 'blockquote'])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    pricing_model = models.CharField(max_length=255, choices=PricingModel.choices, default=PricingModel.HOURLY)
    cta = models.CharField('Call to Action', max_length=255, default='Order Now')
    cta_url = models.URLField(blank=True)
    pre_cta = models.CharField('Call to Action (Before Page)', max_length=255, default='Learn More', help_text='The Call to action BEFORE ')
    related_service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True)
    redirect_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('icon'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('cta'),
            FieldPanel('cta_url'),
            FieldPanel('pre_cta'),
        ], heading='Call to Action'),
        MultiFieldPanel([
            FieldPanel('price'),
            FieldPanel('pricing_model'),
        ], heading='pricing'),
    ]

    parent_page_types = ['services.ServiceCollection']

    class Meta:
        verbose_name = 'Service'

    def __str__(self):
        return self.title

    def get_price(self):
        price = f'${self.price}'
        return price


class ServiceCollection(Page):
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('icon'),
        FieldPanel('image'),
    ]

    parent_page_types = ['base.HomePage', 'services.ServiceCollection']

    class Meta:
        verbose_name_plural = 'Service Collections'

    def get_context(self, request):
        context = super().get_context(request)
        context['collections'] = ServiceCollection.objects.live()
        context['services'] = self.get_descendants().type(Service).live().order_by('title')
        return context

    def __str__(self):
        return self.title

    def get_icon(self):
        try:
            return self.icon.get_rendition('fill-50x50').img_tag()
        except:
            return ''
    get_icon.short_description = 'icon'



class Testimonial(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name='testimonials')
    author_first_name = models.CharField(max_length=50)
    author_last_name = models.CharField(max_length=50)
    author_bio = models.CharField(max_length=255)
    author_profile_image = models.ImageField(upload_to='testimonials/author-images/', blank=True, null=True)
    star_rating = models.IntegerField(choices=(((x, x) for x in range(1, 6))), default=5)
    heading = models.CharField(max_length=255)
    body = models.TextField()
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    live = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('author'),
            FieldPanel('author_first_name'),
            FieldPanel('author_last_name'),
            FieldPanel('author_bio'),
            FieldPanel('author_profile_image'),

        ], heading='Author'),
        MultiFieldPanel([
            FieldPanel('star_rating'),
            FieldPanel('heading'),
            FieldPanel('body'),
        ], heading='content'),
        FieldPanel('service'),
        FieldPanel('live'),
    ]

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.heading
 
    def get_author_name(self):
        return f'{self.author_first_name} {self.author_last_name}'
    get_author_name.short_description = 'Author name'

    
