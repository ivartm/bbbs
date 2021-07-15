from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from bbbs.questions.filters import QuestionFilter
from bbbs.questions.models import Question, QuestionTag
from bbbs.questions.serializers import (
    QuestionSerializer,
    QuestionTagSerializer,
)


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

    queryset = (
        QuestionTag.objects.exclude(questions=None).distinct().order_by("id")
    )
    serializer_class = QuestionTagSerializer
    permission_classes = [AllowAny]
