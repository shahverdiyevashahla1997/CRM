from django.db import models

class Service(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["name"]
        permissions = [("manage_services", "Can manage services")]

    def __str__(self):
        return self.name
