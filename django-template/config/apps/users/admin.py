from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_full_name')


    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'full name'
