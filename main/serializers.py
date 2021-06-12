from main.models import Main
from rest_framework import serializers
from places.serializers import PlaceSerializerRead
from questions.serializers import QuestionSerializer


class MainSerializer(serializers.ModelSerializer):
    place = PlaceSerializerRead()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Main
        fields = ["place", "questions"]
