from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['name', 'service', 'document', 'signed_date', 'start_date', 'end_date', 'amount', 'lead']
        widgets = {'signed_date': forms.DateInput(attrs={'type': 'date'}), 'start_date': forms.DateInput(attrs={'type': 'date'}), 'end_date': forms.DateInput(attrs={'type': 'date'})}
