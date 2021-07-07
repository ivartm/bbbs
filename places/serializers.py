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
        exclude = ("published",)

    def create(self, validated_data):
        return Place.objects.create(**validated_data)

    def get_gender(self, obj):
        return obj.get_gender_display()

    # def validate(self, data):
    #     question = data.get("question")
    #     request = self.context.get("request")
    #     if request.method == "POST":
    #         if not question:
    #             raise serializers.ValidationError(
    #                 {"question": "Пожалуйста, введите вопрос"}
    #             )
    #         elif len(question) < 30:
    #             raise serializers.ValidationError(
    #                 {"question": "Задайте более развёрнутый вопрос"}
    #             )
    #     return data
