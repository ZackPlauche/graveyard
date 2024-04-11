from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    fields = (
        ('name', 'active')
    )
    list_editable = ('active', )


@admin.register(Streamer)
class StreamerAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_editable = ('category', )
    search_fields = ('name', 'category')
    fields = (('name', 'category'))



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'description', 'live', 'followers', 'streamer', 'platform', 'monitor']
    search_fields = ('name', 'full_name', 'description', 'streamer__name')
    list_filter = ('platform', 'live')
    fields = (
        ('name', 'monitor', 'live'),
        'streamer',
        'platform',
        'profile_pic_url',
        'full_name',
        'description',
        'followers_data',
        'followers'
    )


@admin.register(APIAccount)
class APIAccountAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'platform',
        'username',
        'password',
        'blacklist',
        'client_id',
        'api_key',
        'auth_token'
    ]


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = [
        'broadcast_id',
        'host',
        'platform',
        'title',
        'start_time',
        'end_time',
        'duration',
        'live',
        'current_viewers',
        'peak_viewers',
        'average_viewers',
        'score',
        'shady',
    ]
    list_filter = ('platform', 'live')
    search_fields = ('host__name', 'title', 'broadcast_id')
    fieldsets = (
        (None, {
            'fields': (
                'broadcast_id',
                'host',
                'platform',
                'title',
                (
                    'start_time',
                    'end_time'
                ),
                'live',
                'shady',
            ),
        }),
        ('Raw Stream Data', {
            'fields': ('viewer_data', 'likes_data'),
            'classes': ('collapse',)
        }),
        ('Stream Data', {
            'fields': (
                (
                    'average_viewers',
                    'cumulative_viewers',
                    'current_viewers',
                    'peak_viewers',
                ),
                'score',
                'update_time',
                'url',
                'cover_frame_url',
                'cobroadcasters',
            ),
        }),
    )
