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
        many=True, read_only=True, slug_field="slug"
    )

    class Meta:
        model = Right
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "slug"}}
