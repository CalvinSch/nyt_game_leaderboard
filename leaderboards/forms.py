from django import forms
from .models import Game, ConnectionsScore

class ConnectionsScoreForm(forms.ModelForm):
    class Meta:
        model = ConnectionsScore
        fields = [
            'raw_score_details'
        ]
        widgets = {
            'raw_score_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }