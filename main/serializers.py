from rest_framework import serializers

from main.models import Main
from places.serializers import PlaceSerializer
from questions.serializers import QuestionSerializer


class MainSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Main
        fields = ["place", "questions"]
