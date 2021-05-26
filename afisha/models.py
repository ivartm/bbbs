from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.utils import timezone

from common.models import City

User = get_user_model()


class Event(models.Model):
    address = models.CharField(
        max_length=200,
        verbose_name="Адрес"
    )
    contact = models.CharField(
        max_length=200,
        verbose_name="Контакт"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Дополнительная информация"
    )
    startAt = models.DateTimeField(
        verbose_name="Начало"
    )
    endAt = models.DateTimeField(
        verbose_name="Окончание"
    )
    seats = models.PositiveIntegerField(
        verbose_name="Свободные места"
    )
    city = models.ForeignKey(
        City,
        related_name="events",
        on_delete=models.RESTRICT,
        verbose_name="Город"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["startAt"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def clean(self):
        if self.startAt > self.endAt:
            raise ValidationError({
                'end_at': 'Проверьте дату: не может быть меньше даты начала'
            })
        if self.startAt < timezone.now():
            raise ValidationError({
                'start_at': 'Проверьте дату: не может быть меньше текущей'
            })


class EventParticipant(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="eventparticipants",
        null=True,
        verbose_name="Участник"
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.RESTRICT,
        related_name="eventparticipants",
        verbose_name="Мероприятие"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "event"], name="unique_participant"
            )
        ]
        ordering = ["-event"]
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
