from django import forms
from .models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'service', 'channel', 'budget', 'is_active', 'start_date', 'end_date']
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}), 'end_date': forms.DateInput(attrs={'type': 'date'})}
