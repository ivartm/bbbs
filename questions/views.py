from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from common.filters import QuestionFilter
from questions.models import Question, QuestionTag
from questions.serializers import QuestionSerializer, QuestionTagSerializer


class QuestionsList(ListCreateAPIView):
    queryset = (
        Question.objects.exclude(answer__exact="")
        .all()
        .prefetch_related("tags")
    )
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestionFilter

    # def get(self, request):
    #     paths = {
    #         '/api/v1/questions/': QuestionTag.objects.get,
    #     }
    #     for key, value in paths.items():
    #         if self.path == key:
    #             print(value(id=1))


class QuestionsTagList(ListAPIView):
    queryset = QuestionTag.objects.all().order_by("name")
    serializer_class = QuestionTagSerializer
    permission_classes = [AllowAny]
