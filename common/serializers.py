from datetime import datetime

from petrovich.enums import Case
from petrovich.main import Petrovich
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from common.models import City, Meeting


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class MeetingSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    place = serializers.CharField(max_length=50, min_length=2)
    description = serializers.CharField(max_length=5000, min_length=2)
    date = serializers.DateField()

    def validate(self, data):
        if "date" in data:
            if data["date"] > datetime.now().date():
                raise serializers.ValidationError(
                    "date can not be more than today"
                )
            return data
        return data

    def get_name(self, obj):
        if obj.user.profile.curator is None:
            return None
        change_ending = Petrovich()
        return (
            change_ending.firstname(
                value=obj.user.profile.curator.first_name,
                case=Case.DATIVE,
                # gender=user.profile.curator.gender,
            )
            + " "
            + obj.user.profile.curator.last_name[0]
            + "."
        )

    class Meta:
        model = Meeting
        fields = "__all__"
        read_only_fields = ["user"]


class MeetingMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
