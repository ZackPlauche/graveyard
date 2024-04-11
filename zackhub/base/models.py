from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from wagtail.admin.panels import (FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList, PageChooserPanel)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Page
from wagtail.fields import StreamField
from django.contrib import messages

from .blocks import SectionStreamBlock
from users.forms import ContactForm


class HomePage(Page):
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_cta_url = models.ForeignKey('wagtailcore.Page', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    hero_background_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    body = StreamField(SectionStreamBlock(required=False), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title', classname="title"),
            FieldPanel('hero_subtitle'),
            PageChooserPanel('hero_cta_url'),
        ], heading='Hero Content', classname='collapsed collapsible'),
        FieldPanel('body'),
    ]

    parent_page_types = ['wagtailcore.Page']
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        context['form'] = ContactForm()
        return context

    def serve(self, request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                messages.error(request, 'The information you put in this form wasn\'t valid.')
        return super().serve(request)


@register_setting(icon='mail')
class SiteInfoSettings(BaseSiteSetting):
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    facebook_url = models.URLField('Facebook URL', blank=True)
    github_url = models.URLField('GitHub URL', blank=True)
    instagram_url = models.URLField('Instagram URL', blank=True)
    linkedin_url = models.URLField('LinkedIn URL', blank=True)
    twitter_url = models.URLField('Twitter URL', blank=True)
    youtube_url = models.URLField('YouTube URL', blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone_number'),
        ]),
    ]

    social_panels = [
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('instagram_url'),
            FieldPanel('linkedin_url'),
            FieldPanel('github_url'),
            FieldPanel('youtube_url'),
            FieldPanel('twitter_url'),
        ])
    ]

    edit_handler = TabbedInterface([
        ObjectList(panels, heading='General'),
        ObjectList(social_panels, heading='Social Links'),
    ])

    class Meta:
        verbose_name = 'Contact Info'

    def __str__(self):
        return f'{self.site.site_name} SocialMediaSettings'
