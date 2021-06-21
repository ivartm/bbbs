from rest_framework import serializers

from rights.models import Right, RightTag


class RightTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightTag
        exclude = [
            "id",
        ]


class RightSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Right
        fields = "__all__"
