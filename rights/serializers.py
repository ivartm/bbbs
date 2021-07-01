from rest_framework import serializers

from rights.models import Right, RightTag


class RightTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightTag
        fields = "__all__"


class RightSerializer(serializers.ModelSerializer):
    tags = RightTagSerializer(many=True, read_only=True)

    class Meta:
        model = Right
        fields = "__all__"
