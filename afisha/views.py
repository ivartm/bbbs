from django.db.models import Count
from django.shortcuts import get_list_or_404
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from afisha.models import Event, EventParticipant
from afisha.serializers import EventParticipantSerializer, EventSerializer
from users.models import Profile
from django.shortcuts import get_object_or_404

# class CrudToEventParticipantViewSet(
#     CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
# ):
#     pass


# class EventParticipantViewSet(CrudToEventParticipantViewSet):
#     serializer_class = EventParticipantSerializer
#     permission_classes = [IsAuthenticated]
#     search_fields = [
#         "event",
#     ]

#     def get_queryset(self):
#         user = self.request.user
#         queryset = EventParticipant.objects.filter(user=user)
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class EventViewSet(
    GenericViewSet,
    ListModelMixin,
    # generics.ListAPIView,
  ):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        queryset = (
            Event.objects.filter(city=profile.city)
            .annotate(taken_seats=(Count("eventparticipant")))
            .order_by("start_at")
        )
        return queryset

    @action(
        methods=["get", "post", "delete"],
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=EventParticipantSerializer,
        url_path="event-participants",
        url_name="participants",
    )
    def event_participant(self, request):
        serializer = self.get_serializer_class()

        if request.method == "GET":
            user = self.request.user
            queryset = get_list_or_404(EventParticipant, user=user)
            # queryset = EventParticipant.objects.filter(user=user)
            data = serializer(queryset, many=True)
            return Response(data.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        # serializer_data = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            serializer.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
