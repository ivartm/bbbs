from rest_framework import serializers

from bbbs.rights.models import Right, RightTag


class RightTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightTag
        fields = "__all__"


class RightSerializer(serializers.ModelSerializer):
    tags = RightTagSerializer(many=True, read_only=True)
    color = serializers.SerializerMethodField("get_colorname")

    def get_colorname(self, obj):
        color_dict = {
            "#E9D379": "yellow",
            "#AAD59E": "green",
            "#DF9687": "pink",
            "#CDD2FA": "blue",
        }
        return color_dict[obj.color]

    class Meta:
        model = Right
        fields = "__all__"
