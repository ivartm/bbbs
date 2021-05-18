from rest_framework import generics, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated

from afisha.models import Event, EventParticipant
from users.models import Profile
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
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user.id)
        queryset = Event.objects.filter(
            city_id=profile.city.id
        ).order_by('start_at')
        return queryset
