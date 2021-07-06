from rest_framework.serializers import ModelSerializer

from common.models import City, Meeting
from users.models import Profile


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class MyCitySerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "id", "city"
        lookup_field = "city"


class MeetingSerializer(ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        read_only_fields = ["user"]
