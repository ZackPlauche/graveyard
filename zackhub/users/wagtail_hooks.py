from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register,
)

from .models import Message

class MessageAdmin(ModelAdmin):
    model = Message
    menu_icon = 'mail'
    menu_label = 'Messages'
    menu_order = 103
    list_display = ('author_email', 'author_full_name', 'message', 'date_created', 'read')
    list_filter = ('read', 'date_created')

    def author_email(self, obj):
        return obj.author.__str__()
    author_email.short_description = 'email'

    def author_full_name(self, obj):
        return obj.author.get_full_name()
    author_full_name.short_description = 'full name'
    

modeladmin_register(MessageAdmin)