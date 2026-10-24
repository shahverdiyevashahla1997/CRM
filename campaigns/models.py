from django.db import models
from services.models import Service

class Campaign(models.Model):
    CHANNELS = [
        ("social", "Социальные сети"), ("search", "Поисковая реклама"),
        ("email", "Email-рассылка"), ("offline", "Офлайн"), ("other", "Другое"),
    ]
    name = models.CharField("Название кампании", max_length=180, unique=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="campaigns", verbose_name="Услуга")
    channel = models.CharField("Канал продвижения", max_length=20, choices=CHANNELS)
    budget = models.DecimalField("Рекламный бюджет", max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField("Активна", default=True)
    start_date = models.DateField("Дата начала", null=True, blank=True)
    end_date = models.DateField("Дата окончания", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
