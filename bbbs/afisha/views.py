from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from bbbs.afisha.filters import EventFilter
from bbbs.afisha.models import Event, EventParticipant
from bbbs.afisha.serializers import EventParticipantSerializer, EventSerializer
from bbbs.common.utils.months_helpers import month_name_by_number

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
    """Lists all not finished events in user's city.

    Could be filtered by month's number. Supports multiple comma seppareted
    values.
    """

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = Event.afisha_objects.not_finished_user_afisha(user=user)
        return queryset.order_by("start_at")


class MonthAPIView(generics.GenericAPIView):
    """List of months with at least one non finished event in users's city."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        values_qs = Event.afisha_objects.user_afisha_months(user=user)

        list_of_months = [
            {
                "id": month_id,
                "name": month_name_by_number(month_id),
            }
            for month_id in values_qs
        ]

        return JsonResponse(
            list_of_months,
            safe=False,
            status=status.HTTP_200_OK,
        )
