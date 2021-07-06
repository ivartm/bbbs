from django.db.models import CharField, Value
from petrovich.enums import Case
from petrovich.main import Petrovich
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from common.models import City, Meeting
from common.permissions import IsOwner
from common.serializers import (
    CitySerializer,
    MeetingSerializer,
    MyCitySerializer,
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
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.curator is not None:
            change_ending = Petrovich()
            name = (
                change_ending.firstname(
                    value=user.profile.curator.first_name,
                    case=Case.DATIVE,
                    gender=user.profile.curator.gender,
                )
                + " "
                + user.profile.curator.last_name[0]
                + "."
            )
            queryset = Meeting.objects.filter(user=user).annotate(
                name=Value(name, output_field=CharField())
            )
        else:
            queryset = Meeting.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
