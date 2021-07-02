from rest_framework.generics import ListAPIView
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from common.models import City, Meeting
from common.serializers import (
    CitySerializer,
    MyCitySerializer,
    MeetingSerializer,
)
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


class MeetingAPIView(
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    RetrieveModelMixin,
):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Meeting.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
