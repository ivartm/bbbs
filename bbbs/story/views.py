from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny

from bbbs.story.models import Story
from bbbs.story.serializers import StorySerializer


class StoryList(RetrieveModelMixin, ListAPIView):
    queryset = Story.objects.all().order_by("id")
    serializer_class = StorySerializer
    permission_classes = [AllowAny]
