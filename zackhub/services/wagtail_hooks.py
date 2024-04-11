from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register,
)

from services.models import Service, ServiceCollection, Testimonial


class ServiceAdmin(ModelAdmin):
    model = Service
    menu_label = 'Services'
    menu_icon = 'fa-briefcase'
    list_display = ('title', 'price', 'get_icon')
    search_fields = ('title', )

    def get_icon(self, obj):
        try:
            return obj.icon.get_rendition('fill-50x50').img_tag()
        except:
            return ''
    get_icon.short_description = 'icon'


class ServiceCollectionAdmin(ModelAdmin):
    model = ServiceCollection
    menu_icon = 'folder-open-1'
    list_display = ('title', 'get_icon')

class TestimonialAdmin(ModelAdmin):
    model = Testimonial
    menu_icon = 'pick'
    list_display = ('heading', 'get_author_name', 'live')


class ServiceModelAdminGroup(ModelAdminGroup):
    menu_label = 'Services'
    menu_icon = 'fa-briefcase'
    menu_order = 101
    items = (ServiceAdmin, ServiceCollectionAdmin, TestimonialAdmin)


modeladmin_register(ServiceModelAdminGroup)
