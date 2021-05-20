from django.db.models import Count
from rest_framework import generics
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from afisha.models import Event, EventParticipant
from afisha.serializers import EventParticipantSerializer, EventSerializer
from users.models import Profile


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

    def perform_destroy(self, instance):
        instance.delete()


class EventViewSet(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user_id=self.request.user.id)
        queryset = (
            Event.objects.filter(city_id=profile.city.id)
            .annotate(taken_seats=(Count("eventparticipant")))
            .order_by("start_at")
        )
        return queryset
