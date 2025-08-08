# admin.py
from django.contrib import admin
from .models import ScheduledTask

@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'run_at', 'executed')
    list_filter = ('executed',)
    search_fields = ('name',)
    ordering = ('-run_at',)
