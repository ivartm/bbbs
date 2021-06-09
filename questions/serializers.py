from rest_framework import serializers

from questions.models import Question, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        lookup_field = "name"


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    answer = serializers.CharField(read_only=True)
    pubDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Question
        fields = serializers.ALL_FIELDS

    def to_internal_value(self, data):
        question = data.get("question")
        if Question.objects.filter(question=question).exists():
            raise serializers.ValidationError(
                {"question": "Такой вопрос уже задавали"}
            )
        return {"question": question}

    def validate(self, data):
        question = data.get("question")
        request = self.context.get("request")
        if request.method == "POST":
            if not question:
                raise serializers.ValidationError(
                    {"question": "Пожалуйста, введите вопрос"}
                )
            elif len(question) < 30:
                raise serializers.ValidationError(
                    {"question": "Задайте более развёрнутый вопрос"}
                )
        return data
