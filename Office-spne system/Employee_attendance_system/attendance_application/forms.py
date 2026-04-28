from django import forms
from .models import AttendanceRecord


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['photo', 'remark', 'location', 'latitude', 'longitude', 'fence']
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Remark for Clock Out'}),
            'location': forms.TextInput(attrs={'readonly': 'readonly'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'fence': forms.Select(choices=[
                ('', '--Select--'),
                ('main', 'Main Gate'),
                ('back', 'Back Gate'),
            ])
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise forms.ValidationError("This field is required.")
        return photo
