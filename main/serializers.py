from rest_framework import serializers

from entertainment.models import Article
from main.models import Main
from places.serializers import PlaceSerializer
from questions.serializers import QuestionSerializer


class ArticleMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "color"]


class MainSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    questions = QuestionSerializer(many=True)
    articles = ArticleMainSerializer(many=True)

    class Meta:
        model = Main
        fields = ["place", "questions", "articles"]
