from rest_framework import serializers

from questions.models import Question
from common.serializers import TagSerializer


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    question = serializers.CharField()
    answer = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = serializers.ALL_FIELDS
