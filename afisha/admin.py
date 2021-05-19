from django.contrib.admin import register
from django.contrib import admin

from afisha.models import Event, EventParticipant


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "contact",
        "title",
        "description",
        "start_at",
        "end_at",
        "seats",
        "taken_seats",
        "city",
    )
    empty_value_display = "-пусто-"


@register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "event")
    empty_value_display = "-пусто-"
