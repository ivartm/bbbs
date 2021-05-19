from rest_framework import serializers
from afisha.models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    booked = serializers.SerializerMethodField("is_booked")

    def is_booked(self, instanse):
        if EventParticipant.objects.filter(
            event=Event.objects.get(id=instanse.id)   # Неправильно. Выдает все евенты на которые хоть кто нибудь придет
        ).exists():
            return True
        return False

    class Meta:
        model = Event
        fields = "__all__"


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ("id", "event")
        lookup_field = "event"
