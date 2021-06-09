from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from questions.models import Question, Tag
from questions.serializers import QuestionSerializer, TagSerializer


class QuestionsList(ListCreateAPIView):
    queryset = Question.objects.exclude(answer__exact="").all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("tag", "tag__name")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Success": "Спасибо! Мы приняли ваш вопрос."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class QuestionsTagList(ListAPIView):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
