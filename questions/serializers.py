from rest_framework import serializers

from questions.models import Question, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        lookup_field = 'slug'


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField(read_only=True)
    pubDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Question
        fields = serializers.ALL_FIELDS
