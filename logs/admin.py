from django.contrib import admin
from .models import Log

# Register your models here.

class LogAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "status", "event_type", "timestamp")
    search_fields = ("user__username", "ip_address", "status", "event_type")
    list_filter = ("status", "event_type", "timestamp")
    

admin.site.register(Log, LogAdmin)  