from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from users.models import Profile

from afisha.models import Event, EventParticipant
from afisha.serializers import EventParticipantSerializer, EventSerializer


class CrudToEventParticipantViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


class EventParticipantViewSet(CrudToEventParticipantViewSet):
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


class EventViewSet(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(Profile, user_id=self.request.user.id)
        subquery = EventParticipant.objects.filter(
            user=profile.user, event=OuterRef("pk")
        )
        queryset = (
            Event.objects.filter(city=profile.city)
            .annotate(taken_seats=(Count("event_participants")))
            .annotate(booked=Exists(subquery))
            .order_by("startAt")
        )

        return queryset
