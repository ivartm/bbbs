from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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


class Meeting(models.Model):
    BAD = "bad"
    GOOD = "good"
    NEUTRAL = "neutral"

    SMILE_TYPE_CHOICES = [
        (BAD, "bad"),
        (GOOD, "good"),
        (NEUTRAL, "neutral"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="meetings",
        verbose_name="Наставник",
    )

    image = models.ImageField(
        upload_to="meetings/",
        verbose_name="Фото",
        help_text="Загрузите фото",
        blank=True,
    )
    description = models.TextField(
        max_length=5000,
        verbose_name="Описание",
        help_text="Краткое описание",
    )

    smile = models.CharField(choices=SMILE_TYPE_CHOICES, max_length=20)

    place = models.CharField(max_length=50)
    date = models.DateField(verbose_name="Дата", blank=True)
    sendToCurator = models.BooleanField(default=False)

    class Meta:
        ordering = ("-date",)
        verbose_name_plural = "Встречи"
        verbose_name = "Встреча"

    def __str__(self):
        return f"{self.place}, {self.date}"
