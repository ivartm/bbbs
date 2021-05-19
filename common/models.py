from django.db import models
from django.contrib.auth import get_user_model


class City(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Город',
        help_text='Введите город',
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Приоритет вывода',
        help_text='Укажите, если город должен иметь приоритетный вывод'
    )

    def __str__(self):
        return self.name
