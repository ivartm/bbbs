from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from afisha.models import Event, EventParticipant
from users.models import Profile


class EventSerializer(serializers.ModelSerializer):
    booked = serializers.BooleanField(read_only=True)
    taken_seats = serializers.IntegerField(read_only=True)

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
        taken_seats = event.event_participants.count()
        seats = event.seats
        end_event = event.end_at
        if request.method == "POST":
            if event.city != profile.city:
                raise serializers.ValidationError(
                    {"message": "Извините, но мероприятие не в Вашем городе."}
                )
            if end_event < timezone.now():
                raise serializers.ValidationError(
                    {"message": "Мероприятие уже закончилось."}
                )
            if taken_seats >= seats:
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
