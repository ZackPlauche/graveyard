from django.contrib import admin

from .models import Restaurant, Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    fields = ('id', 'title', 'description', 'price')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'logo')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'restaurant')
    list_filter = ('restaurant', )
    list_editable = ('title', )
    inilnes = (MenuItemInline, )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'menu', 'restaurant')
    list_filter = ('menu', )

    def restaurant(self, obj):
        return obj.menu.restuarant