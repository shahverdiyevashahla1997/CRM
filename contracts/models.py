from django.db import models
from services.models import Service
from leads.models import Lead

class Contract(models.Model):
    name = models.CharField("Название контракта", max_length=180)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="contracts", verbose_name="Услуга")
    document = models.FileField("Документ", upload_to="contracts/", blank=True)
    signed_date = models.DateField("Дата заключения")
    start_date = models.DateField("Начало действия")
    end_date = models.DateField("Окончание действия")
    amount = models.DecimalField("Сумма", max_digits=12, decimal_places=2)
    lead = models.ForeignKey(Lead, on_delete=models.PROTECT, null=True, blank=True, related_name="contracts", verbose_name="Потенциальный клиент")

    class Meta:
        ordering = ["-signed_date"]

    def __str__(self):
        return self.name
