from django.db import models
from campaigns.models import Campaign

class Lead(models.Model):
    full_name = models.CharField("Ф. И. О.", max_length=200)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email")
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT, related_name="leads", verbose_name="Рекламная кампания")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name

    @property
    def is_active_client(self):
        return hasattr(self, "active_client")
