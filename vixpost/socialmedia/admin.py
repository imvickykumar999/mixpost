from django.contrib import admin
from django.utils.html import format_html
from .models import ScheduledTask

@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'run_at', 'executed', 'media_preview')
    readonly_fields = ('media_preview',)

    def media_preview(self, obj):
        if obj.media:
            file_url = obj.media.url
            if obj.media.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                return format_html('<img src="{}" width="100" height="100" style="object-fit:contain;" />', file_url)
            elif obj.media.name.lower().endswith(('.mp4', '.webm', '.ogg')):
                return format_html('''
                    <video width="200" height="150" controls>
                        <source src="{}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                ''', file_url)
            else:
                return format_html('<a href="{}" target="_blank">Download File</a>', file_url)
        return "-"
    
    media_preview.short_description = 'Media Preview'
