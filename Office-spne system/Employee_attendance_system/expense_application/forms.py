from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'claim_type',
            'travel_type',
            'city',
            'date',
            'expense',
            'currency',
            'conversion_rate',
            # 'unit_value',
            'amount',
            'final_amount',
            'project',
            'document',
            'bill',
            'remarks'
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }