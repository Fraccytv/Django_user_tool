from django.contrib import admin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    # list_filter = ('is_active', 'is_staff')
    # ordering = ('-date_joined',)    
admin.site.register(CustomUser, CustomUserAdmin)