from rest_framework import serializers

from bbbs.questions.models import Question, QuestionTag


class QuestionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTag
        fields = "__all__"
        lookup_field = "name"


class QuestionSerializer(serializers.ModelSerializer):
    tags = QuestionTagSerializer(many=True, read_only=True)
    answer = serializers.CharField(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

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
