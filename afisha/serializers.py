from rest_framework import serializers
from afisha.models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'
        lookup_field = 'slug'
