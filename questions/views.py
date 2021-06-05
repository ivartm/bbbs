from rest_framework import generics

from questions.models import Question
from questions.serializers import QuestionSerializer


class QuestionsList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
