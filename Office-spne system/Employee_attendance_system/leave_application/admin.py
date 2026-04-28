from django.contrib import admin
from .models import LeaveApplication



class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'from_date', 'to_date', 'total_days', 'applied_at')
    list_filter = ('leave_type', 'applied_at')
    search_fields = ('user__username', 'status')

admin.site.register(LeaveApplication, LeaveApplicationAdmin)



