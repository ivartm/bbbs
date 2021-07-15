from rest_framework import serializers

from bbbs.entertainment.models import Article
from bbbs.entertainment.serializers import MovieSerializer, VideoSerializer
from bbbs.main.models import Main
from bbbs.places.serializers import PlaceSerializer
from bbbs.questions.serializers import QuestionSerializer
from bbbs.story.models import Story


class ArticleMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "color"]


class StoryMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["title", "image_url"]


class MainSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    questions = QuestionSerializer(many=True)
    articles = ArticleMainSerializer(many=True)
    movies = MovieSerializer(many=True)
    history = StoryMainSerializer()
    video = VideoSerializer()

    class Meta:
        model = Main
        fields = [
            "place",
            "questions",
            "articles",
            "movies",
            "history",
            "video",
        ]
