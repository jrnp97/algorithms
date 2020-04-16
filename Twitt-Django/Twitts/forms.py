from django import forms
from .models import Twitts

class TwittForm(forms.ModelForm):

    class Meta:
        model = Twitts
        fields = [
            'texto',
        ]

        labels = {
            'texto':'¿ Que estas pensando ?',
        }

        widgets = {
            'texto': forms.Textarea(attrs={'class':'form-control'}),
        }