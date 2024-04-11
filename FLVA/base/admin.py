from django.contrib import admin
from .models import Post, Contact, FAQ, AboutSection, Event
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name']

admin.site.register(FAQ)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'display', 'pub_date', 'contains_image']

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'display']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'display', 'date', 'type', 'contains_image']
