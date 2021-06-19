from rest_framework import serializers

from .models import Place, PlaceTag


class PlaceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceTag
        fields = "__all__"


class InfoField(serializers.ReadOnlyField):
    def to_representation(self, place):
        display = ""
        if place.gender:
            display += place.get_gender(place.gender) + ", "
        display += str(place.age) + " лет. "
        display += place.get_activity_type(place.activity_type) + " отдых"
        return display


class PlaceSerializerRead(serializers.ModelSerializer):
    info = InfoField(source="*")
    tag = PlaceTagSerializer(many=True)

    class Meta:
        model = Place
        exclude = (
            "age",
            "gender",
            "activity_type",
        )

    def get_gender(self, obj):
        return obj.get_gender_display()


class PlaceSerializerWrite(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        many=True, queryset=PlaceTag.objects.all(), slug_field="slug"
    )

    class Meta:
        model = Place
        exclude = ("id",)
