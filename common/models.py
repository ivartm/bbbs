from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=30)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
