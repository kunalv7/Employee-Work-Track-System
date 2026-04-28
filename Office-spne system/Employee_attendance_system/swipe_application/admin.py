from django.contrib import admin
from .models import SwipeApplication

class SwipeApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager', 'category', 'status', 'applied_at')
    list_filter = ('status', 'manager')
    search_fields = ('user__username', 'manager__username')

admin.site.register(SwipeApplication, SwipeApplicationAdmin)