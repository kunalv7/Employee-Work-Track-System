from django import forms
from .models import LeaveApplication

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['period', 'from_date', 'to_date', 'start_day', 'end_day',
                  'half_start', 'half_end', 'leave_type', 'total_days', 'reason', 'document']

        widgets = {
            'total_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'text'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'text'}),
            'period': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }
