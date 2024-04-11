from django.contrib import admin
from django.contrib.auth import models as auth_models
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_search = ['email']


admin.site.unregister(auth_models.Group)