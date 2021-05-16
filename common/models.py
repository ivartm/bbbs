from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.base import Model

User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=30)
    is_primary = models.BooleanField(default=False)   # Noqa не совсем понятен параметр

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"