from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import ScheduledTask

MAX_CAPTION_LENGTH = 500

class ScheduledTaskForm(forms.ModelForm):
    class Meta:
        model = ScheduledTask
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['caption'].widget.attrs.update({
            'maxlength': MAX_CAPTION_LENGTH,
            'oninput': 'updateCharCount(this)',
            'style': 'width: 90%;',
            'rows': 4,
        })
        # Optional: update help_text dynamically or just leave static in models.py
        self.fields['caption'].help_text = f"Caption text (max {MAX_CAPTION_LENGTH} characters)."


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    form = ScheduledTaskForm
    list_display = ('name', 'run_at', 'executed', 'url_generated', 'media_preview')
    list_editable = ('executed',)
    readonly_fields = ('media_preview', 'url_generated')
    list_display_links = ('name',)

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

    def url_generated(self, obj):
        if obj.url_generated:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.url_generated, obj.url_generated)
        return "-"
    url_generated.short_description = "Mastodon URL"

    class Media:
        js = ('admin/js/caption_charcount.js',)
