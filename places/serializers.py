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


class PlaceSerializer(serializers.ModelSerializer):
    info = InfoField(source="*")
    tags = PlaceTagSerializer(many=True, read_only=True)
    gender = serializers.CharField(
        write_only=True, required=False, max_length=1
    )

    class Meta:
        model = Place
        read_only_fields = ("tags", "chosen")
        exclude = ["published"]

    def create(self, validated_data):
        validated_data["chosen"] = True
        return Place.objects.create(**validated_data)

    def get_gender(self, obj):
        return obj.get_gender_display()
