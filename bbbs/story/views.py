from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from bbbs.story.models import Story
from bbbs.story.serializers import StorySerializer


class StoryList(ListAPIView):
    queryset = Story.objects.all().order_by("id")
    serializer_class = StorySerializer
    permission_classes = [AllowAny]