from django.contrib import admin

from .models import Service, Task

# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform_version')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed', 'provisioner_1', 'provisioner_2', 'service', 'version')
    list_filter = ('completed', 'provisioner_1', 'provisioner_2', 'service')
    list_editable = ('completed',)
    search_fields = ('name', 'provisioner_1', 'provisioner_2', 'service')