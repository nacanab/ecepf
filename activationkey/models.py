# models.py
from django.db import models
from django.utils import timezone

class ActivatedDevice(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    activation_key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Date d'expiration de la clé

    def __str__(self):
        return f"{self.serial_number} - {self.activation_key}"

    def is_expired(self):
        return timezone.now() > self.expires_at