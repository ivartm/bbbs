from rest_framework.serializers import ModelSerializer, BooleanField

from .models import City


class CitySerializer(ModelSerializer):
    isPrimary = BooleanField(source="is_primary")

    class Meta:
        model = City
        fields = "id", "name", "isPrimary"
