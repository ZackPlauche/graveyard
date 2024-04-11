from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'position', 'display']
    list_filter = ('page',)
    fields = (
        ('page', 'section_type'),
        ('title', 'display'),
        'position',
        ('image', 'subtitle'),
        ('button_1_link', 'button_1_text', 'button_2_link', 'button_2_text'),
    )


