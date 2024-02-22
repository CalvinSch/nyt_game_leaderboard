from django import forms
from .models import Game, ConnectionsScore

class ConnectionsScoreForm(forms.ModelForm):
    class Meta:
        model = ConnectionsScore
        fields = [
            'score_details'
        ]
        widgets = {
            'score_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }