from django.contrib import admin
from .models import Service, ServiceCollection, Testimonial

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'pricing_model', 'cta', 'cta_url', 'live',)
    list_editable = ('price', 'pricing_model', 'cta', 'cta_url', )

@admin.register(ServiceCollection)
class ServiceCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'live')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('heading', 'get_author_name', 'live', 'created_date')
    list_editable = ('live', )
    fieldsets = (
        ('Author', {
            'fields': (
                'author',
                'author_first_name', 
                'author_last_name',
                'author_bio',
                'author_profile_image',
            )
        }),
        ('Content', {
            'fields': (
                'star_rating',
                'heading',
                'body',
            )
        }),
        (None, {
            'fields': ('service', 'live')
        })
    )