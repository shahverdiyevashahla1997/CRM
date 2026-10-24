from django import forms
from django.core.exceptions import ValidationError
from leads.models import Lead
from services.models import Service

class ActiveClientCreateForm(forms.Form):
    lead = forms.ModelChoiceField(queryset=Lead.objects.all(), label="Потенциальный клиент")
    contract_name = forms.CharField(max_length=180, label="Название контракта")
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label="Услуга")
    document = forms.FileField(required=False, label="Документ")
    signed_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Дата заключения")
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Начало действия")
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="Окончание действия")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label="Сумма")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lead"].queryset = Lead.objects.exclude(active_client__isnull=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("start_date") and cleaned.get("end_date") and cleaned["end_date"] < cleaned["start_date"]:
            raise ValidationError("Дата окончания не может быть раньше даты начала.")
        return cleaned
