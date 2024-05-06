from .models import AudioDetail
from django import forms
class AudioDetailForm(forms.ModelForm):
    class Meta:
        model = AudioDetail
        fields = ['audio_file']