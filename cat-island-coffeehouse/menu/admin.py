from django.contrib import admin
from .models import MenuCategory, MenuItem

# Register your models here.
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'display']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'display']
