from django.db import models


class City(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name="Город",
        help_text="Введите город",
        unique=True,
    )
    isPrimary = models.BooleanField(
        default=False,
        verbose_name="Приоритет вывода",
        help_text="Укажите, если город должен иметь приоритетный вывод",
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name
