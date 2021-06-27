from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from afisha.models import Event, EventParticipant
from afisha.serializers import EventParticipantSerializer, EventSerializer


User = get_user_model()


class CreateListDestroyMixin(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
):
    pass


class EventParticipantViewSet(CreateListDestroyMixin, GenericViewSet):
    serializer_class = EventParticipantSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "event",
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = EventParticipant.objects.filter(user=user).order_by("id")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = Event.afisha_objects.not_finished_user_afisha(user=user)
        return queryset.order_by("startAt")
