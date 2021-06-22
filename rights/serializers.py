from rest_framework import serializers

from rights.models import Right, RightTag


class RightTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightTag
        exclude = [
            "id",
        ]


class RightSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        source="tags",
        slug_field="slug",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Right
        exclude = ["tags"]
