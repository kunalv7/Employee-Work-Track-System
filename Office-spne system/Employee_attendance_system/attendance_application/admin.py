from django.contrib import admin
from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'fence','location')
    list_filter = ('fence',)
    search_fields = ('user__username',)

    def remark_short(self, obj):
        return (obj.remark[:50] + "...") if obj.remark and len(obj.remark) > 50 else obj.remark
    remark_short.short_description = 'Remark'
