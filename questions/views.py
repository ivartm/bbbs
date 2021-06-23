from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from questions.filters import QuestionFilter
from questions.models import Question, QuestionTag
from questions.serializers import QuestionSerializer, QuestionTagSerializer


class QuestionsList(ListCreateAPIView):
    queryset = Question.objects.exclude(answer__exact="").all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestionFilter


class QuestionsTagList(ListAPIView):
    queryset = QuestionTag.objects.all().order_by("name")
    serializer_class = QuestionTagSerializer
    permission_classes = [AllowAny]
