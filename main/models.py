from django.db import models
from afisha.models import Event


class Main(models.Model):
    on_view = models.BooleanField(default=False, unique=True)
    event = models.OneToOneField(Event, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Главная страница'

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главные страницы'
