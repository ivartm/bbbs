from rest_framework import serializers

from bbbs.entertainment.models import (
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
    tags = MovieTagSerializer(many=True)
    info = serializers.SerializerMethodField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        exclude = ["producer", "year"]

    def get_info(self, obj):
        return "{}, {} год".format(obj.producer, obj.year)

    def get_link(self, obj):
        watch_id = obj.link.split("watch?v=")
        embed_link = f"https://www.youtube.com/embed/{watch_id[1]}"
        return embed_link


class VideoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTag
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    tags = VideoTagSerializer(many=True)
    link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Video
        exclude = ["creative_url"]

    def get_link(self, obj):
        watch_id = obj.link.split("watch?v=")
        embed_link = f"https://www.youtube.com/embed/{watch_id[1]}"
        return embed_link


class BookTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = ["id", "name", "slug"]


class BookSerializer(serializers.ModelSerializer):
    tag = BookTagSerializer()
    color = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def get_color(self, obj):
        return obj.tag.color


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
