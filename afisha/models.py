from django.db.models import Count, Exists, OuterRef
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

from common.models import City

User = get_user_model()


class EventQuerySet(models.QuerySet):
    def with_takenseats(self):
        return self.annotate(takenSeats=(Count("event_participants")))

    def not_finished_events(self):
        return self.filter(endAt__gt=timezone.now())

    def with_booked(self, user: User):
        subquery = EventParticipant.objects.filter(
            user=user,
            event=OuterRef("pk"),
        )
        qs = self.annotate(booked=Exists(subquery))
        return qs

    def city_afisha(self, city: City):
        qs = self.with_takenseats()
        qs = qs.not_finished_events()
        qs = qs.filter(city=city)
        return qs

    def user_afisha(self, user: User):
        qs = self.city_afisha(city=user.profile.city)
        qs = qs.with_booked(user=user)
        return qs


class Event(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес")
    contact = models.CharField(max_length=200, verbose_name="Контакт")
    title = models.CharField(
        max_length=200, verbose_name="Название", unique=True
    )
    description = models.TextField(verbose_name="Дополнительная информация")
    startAt = models.DateTimeField(verbose_name="Начало")
    endAt = models.DateTimeField(verbose_name="Окончание")
    seats = models.PositiveIntegerField(verbose_name="Свободные места")
    city = models.ForeignKey(
        City,
        related_name="events",
        on_delete=models.RESTRICT,
        verbose_name="Город",
    )

    objects = models.Manager()
    afisha_objects = EventQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["startAt"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def clean(self):
        if self.startAt > self.endAt:
            raise ValidationError(
                {
                    "endAt": (
                        "Проверьте дату окончания мероприятия: "
                        "не может быть меньше даты начала"
                    )
                }
            )
        if self.startAt < timezone.now():
            raise ValidationError(
                {
                    "startAt": (
                        "Проверьте дату начала мероприятия: "
                        "не может быть меньше текущей"
                    )
                }
            )
        if self.seats < 1:
            raise ValidationError(
                {"seats": "Число мест должно быть больше нуля"}
            )


class EventParticipant(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_participants",
        null=True,
        verbose_name="Участник",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.RESTRICT,
        related_name="event_participants",
        verbose_name="Мероприятие",
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

    def clean(self):
        if self.user.profile.city != self.event.city:
            raise ValidationError(
                "Нельзя зарегистрировать участника на событие в другом городе!"
            )
