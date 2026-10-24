from django.db import models
from leads.models import Lead
from contracts.models import Contract

class ActiveClient(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.PROTECT, related_name="active_client", verbose_name="Потенциальный клиент")
    contract = models.OneToOneField(Contract, on_delete=models.PROTECT, related_name="active_client", verbose_name="Контракт")
    activated_at = models.DateTimeField("Дата активации", auto_now_add=True)

    class Meta:
        ordering = ["-activated_at"]

    def __str__(self):
        return self.lead.full_name
