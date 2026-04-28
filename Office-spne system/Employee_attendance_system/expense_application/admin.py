from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project',
        'amount',
        'final_amount',
        'currency',
        'city',
        'date',
    )

    list_filter = (
        'claim_type',
        'travel_type',
        'city',
        'currency',
        'date',
    )

    search_fields = (
        'project',
        'city',
        'remarks',
    )

    ordering = ('-date',)

    readonly_fields = ('final_amount',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('claim_type', 'travel_type', 'city', 'date')
        }),

        ('Expense Details', {
            'fields': ('expense', 'currency', 'conversion_rate')
        }),

        ('Amount Info', {
            'fields': ('unit_value', 'amount', 'final_amount')
        }),

        ('Project Info', {
            'fields': ('project',)
        }),

        ('Files', {
            'fields': ('document', 'bill')
        }),

        ('Remarks', {
            'fields': ('remarks',)
        }),
    )