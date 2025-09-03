# logs/admin.py
from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "status", "event_type", "timestamp")
    search_fields = ("user__username", "ip_address")
    list_filter = ("status", "event_type", "timestamp")
    date_hierarchy = "timestamp"