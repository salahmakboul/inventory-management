from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class InventoryItem(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    sujet = models.CharField("Sujet", max_length=200, default="")
    date_arv = models.DateTimeField("Date d'arrivée", default=timezone.now)
    date_creation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.numero} - {self.sujet}"

