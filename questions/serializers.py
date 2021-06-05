from rest_framework import serializers

from questions.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = serializers.ALL_FIELDS
