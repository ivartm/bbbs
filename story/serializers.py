from rest_framework import serializers

from .models import Story, StoryImage


class StoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryImage
        fields = [
            "image",
        ]


class StorySerializer(serializers.ModelSerializer):
    imagesUrls = StoryImageSerializer(source="stories", many=True)

    class Meta:
        model = Story
        fields = "__all__"
