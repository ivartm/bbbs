from django.views import generic
from rest_framework import generics, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated

from afisha.models import Event, EventParticipant
from afisha.serializers import EventSerializer, EventParticipantSerializer


class CrudToEventParticipantViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


# class EventParticipantViewSet(CrudToEventParticipantViewSet):
#     queryset = EventParticipant.objects.all().order_by('-id')
#     serializer_class = EventParticipantSerializer
#     permission_classes = [IsAuthenticated]
#     # filter_backends = [SearchFilter]
#     search_fields = ['event', ]

class EventParticipantViewSet(generics.ListCreateAPIView):
    queryset = EventParticipant.objects.all().order_by('-id')
    serializer_class = EventParticipantSerializer
    permission_classes = [IsAuthenticated]


class EventViewSet(generics.ListAPIView):
    queryset = Event.objects.filter(user=self.request.user).order_by('start_at')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
