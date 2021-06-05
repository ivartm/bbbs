from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from common.models import City, Tag
from common.serializers import CitySerializer, MyCitySerializer, TagSerializer
from users.models import Profile


class CityAPIView(ListAPIView):
    queryset = City.objects.all().order_by("-isPrimary", "name")
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class MyCityApiView(ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MyCitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Profile.objects.filter(user=user)
        return queryset


class TagList(ListAPIView):
    queryset = Tag.objects.all().order_by("-name")
    serializer_class = TagSerializer
