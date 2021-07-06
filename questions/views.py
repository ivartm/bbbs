from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from questions.filters import QuestionFilter
from questions.models import Question, QuestionTag
from questions.serializers import QuestionSerializer, QuestionTagSerializer


class QuestionsAPIView(ListCreateAPIView):
    """Returns only questions with answers."""

    queryset = (
        Question.objects.exclude(answer__exact="")
        .all()
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestionFilter


class QuestionsTagAPIView(ListAPIView):
    """Returns only QuestionTags that used in questions."""

    queryset = QuestionTag.objects.exclude(questions=None).order_by("id")
    serializer_class = QuestionTagSerializer
    permission_classes = [AllowAny]
