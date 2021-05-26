from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from afisha.models import Event, EventParticipant
from users.models import Profile


class EventSerializer(serializers.ModelSerializer):
    booked = serializers.SerializerMethodField("is_booked")
    takenSeats = serializers.IntegerField(read_only=True)

    def is_booked(self, instanse):
        user = self.context["request"].user
        event = get_object_or_404(Event, id=instanse.id)
        if EventParticipant.objects.filter(
            event=event, user_id=user.id
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

    def validate(self, data):
        event = data["event"]
        request = self.context["request"]
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        takenSeats = EventParticipant.objects.filter(event=event).count()
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
            if takenSeats > seats:
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
