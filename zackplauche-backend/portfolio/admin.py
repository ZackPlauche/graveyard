from django.utils.html import format_html
from django.contrib import admin

from .models import Offer, Project, Image, Technology, Review


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'clickable_site_url', 'has_image', 'active', 'featured', 'status')
    list_editable = ('active', 'featured', 'status')
    list_filter = ('active', 'featured', 'status')
    search_fields = ('title',)

    @admin.display(description='Site URL')
    def clickable_site_url(self, obj: Project):
        return format_html(f'<a href="{obj.site_url}" target="_blank">{obj.site_url}</a>')

    @admin.display(description='Image', boolean=True)
    def has_image(self, obj: Project) -> bool:
        return bool(obj.thumbnail)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('alt', 'file', 'url')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'has_icon')

    @admin.display(boolean=True, description='Icon')
    def has_icon(self, obj):
        return bool(obj.icon)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_name', 'source')
    list_editable= ('source', )

    @admin.display(description='Review')
    def review_name(self, obj):
        return str(obj)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'active']
    list_editable = ['active']
