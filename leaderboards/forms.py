from django import forms
from .models import Game, ConnectionsScore

class ConnectionsScoreForm(forms.ModelForm):
    #Need to take player_name as an argument to the form, dynamically retrieved from POST request
    def __init__(self, *args, player_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_name = player_name  # Store the username
        #TODO: Checking/verifying username?
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.player_name = self.player_name  # Set the CharField to the username
        if commit:
            instance.save()
            self.save_m2m()  # Necessary if your model form has many-to-many fields
        return instance

    class Meta:
        model = ConnectionsScore
        fields = [
            'raw_score_details'
        ]
        widgets = {
            'raw_score_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }