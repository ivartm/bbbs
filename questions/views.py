from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from questions.models import Question, Tag
from questions.serializers import QuestionSerializer, TagSerializer


class QuestionsList(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class QuestionsTagList(ListModelMixin, GenericViewSet):
    queryset = Tag.objects.all().order_by("-name")
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
