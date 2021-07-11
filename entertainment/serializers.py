from rest_framework import serializers

from entertainment.models import (
    Article,
    Book,
    BookTag,
    Guide,
    Movie,
    MovieTag,
    Video,
    VideoTag,
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
    tags = VideoTagSerializer(many=True)

    class Meta:
        model = Video
        exclude = ["creative_url"]


class BookTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    tags = BookTagSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
