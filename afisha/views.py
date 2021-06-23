from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.utils import timezone
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
from users.models import Profile


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
        queryset = EventParticipant.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(Profile, user_id=self.request.user.id)
        subquery = EventParticipant.objects.filter(
            user=profile.user, event=OuterRef("pk")
        )
        queryset = (
            Event.objects.filter(city=profile.city, startAt__gt=timezone.now())
            .annotate(takenSeats=(Count("event_participants")))
            .annotate(booked=Exists(subquery))
            .order_by("startAt")
        )

        return queryset
