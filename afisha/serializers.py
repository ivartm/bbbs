from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from users.models import Profile

from afisha.models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    booked = serializers.IntegerField(read_only=True)
    takenSeats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ("id", "event")
        lookup_field = "event"

    def validate(self, data):
        event = data.get("event")
        request = self.context.get("request")
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        takenSeats = event.event_participants.count()
        seats = event.seats
        end_event = event.endAt
        if request.method == "POST":
            if event.city != profile.city:
                raise serializers.ValidationError(
                    {"message": "Извините, но мероприятие не в Вашем городе."}
                )
            if end_event < timezone.now():
                raise serializers.ValidationError(
                    {"message": "Мероприятие уже закончилось."}
                )
            if takenSeats >= seats:
                raise serializers.ValidationError(
                    {"message": "Извините, мест больше нет."}
                )
            if EventParticipant.objects.filter(
                user=user, event=event
            ).exists():
                raise serializers.ValidationError(
                    {"message": "Вы уже зарегистрированы на это мероприятие."}
                )
        return data
