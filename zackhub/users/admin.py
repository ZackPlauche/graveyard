from django.contrib import admin

from .models import Message, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name')

    def full_name(self, obj):
        return obj.get_full_name()

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author_email', 'author_full_name', 'message', 'read')
    list_filter = ('read', )
    list_editable = ('read', )

    def author_email(self, obj):
        return obj.author
    author_email.short_description = 'email'

    def author_full_name(self, obj):
        return obj.author.get_full_name()
    author_full_name.short_description = 'name'