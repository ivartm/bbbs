from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

from common.models import City

User = get_user_model()


class Event(models.Model):
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    seats = models.IntegerField()
    taken_seats = models.IntegerField(default=0)
    city = models.ForeignKey(
        City, related_name="event", on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["start_at"]
        verbose_name = "Событие"
        verbose_name_plural = "События"


class EventParticipant(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="eventparticipant",
        null=True,
    )
    event = models.ForeignKey(
        Event, on_delete=models.RESTRICT, related_name="eventparticipant"
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
