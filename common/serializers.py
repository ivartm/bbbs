from rest_framework.serializers import ModelSerializer

from common.models import City, Tag
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


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
