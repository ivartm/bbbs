from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated

from afisha.models import Event, EventParticipant
from users.models import Profile
from afisha.serializers import EventSerializer, EventParticipantSerializer


class EventParticipantGetPostViewSet(
    CreateModelMixin, ListModelMixin, GenericViewSet
):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = EventParticipant.objects.filter(
            user=self.request.user
        ).order_by("event")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventParticipantDeleteViewSet(DestroyModelMixin, GenericViewSet):
    serializer_class = EventParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = EventParticipant.objects.filter(
            user=self.request.user
        ).order_by("event")
        return queryset


class EventViewSet(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user.id)
        queryset = Event.objects.filter(city_id=profile.city.id).order_by(
            "start_at"
        )
        return queryset
