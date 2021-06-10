from rest_framework import generics

from questions.models import Question, Tag
from questions.serializers import QuestionSerializer, TagSerializer


class QuestionsList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all().order_by("-name")
    serializer_class = TagSerializer
