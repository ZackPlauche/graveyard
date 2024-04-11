from django.contrib import admin
from .models import UserProfile, ExploreSection, Testimonial

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Testimonial)

@admin.register(ExploreSection)
class ExploreSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'display']

