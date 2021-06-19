from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from questions.filters import QuestionFilter
from questions.models import Question, QuestionTag
from questions.serializers import QuestionSerializer, QuestionTagSerializer


class QuestionsList(ListCreateAPIView):
    queryset = Question.objects.exclude(answer__exact="").all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestionFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Success": "Спасибо! Мы приняли Ваш вопрос."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class QuestionsTagList(ListAPIView):
    queryset = QuestionTag.objects.all().order_by("name")
    serializer_class = QuestionTagSerializer
    permission_classes = [AllowAny]
