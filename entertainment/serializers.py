from rest_framework import serializers

from entertainment.models import (
    Guide,
    MovieTag,
    Movie,
    VideoTag,
    Video,
    BookTag,
    Book,
    Article,
)


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = "__all__"


class MovieTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieTag
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class VideoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTag
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class BookTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class EntertainmentSerializer(serializers.ModelSerializer):
    guides = GuideSerializer(many=True)
    movies = MovieSerializer(many=True)
    videos = VideoSerializer(many=True)
    books = BookSerializer(many=True)
    articles = ArticleSerializer(many=True)
