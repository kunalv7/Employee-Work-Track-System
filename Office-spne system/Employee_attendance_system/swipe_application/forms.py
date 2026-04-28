from django import forms
from .models import SwipeApplication

class SwipeApplicationForm(forms.ModelForm):
    class Meta:
        model = SwipeApplication
        fields = ['category', 'request_date', 'in_time', 'out_time', 'reason']
        widgets = {
            'request_date': forms.DateInput(attrs={'type': 'date'}),
            'in_time': forms.TimeInput(attrs={'type': 'time'}),
            'out_time': forms.TimeInput(attrs={'type': 'time'}),
        }