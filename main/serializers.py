from rest_framework import serializers
from main.models import Main
from afisha.serializers import EventSerializer


class MainSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Main
        fields = ('event',)
