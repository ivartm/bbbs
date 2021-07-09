import calendar

from django.contrib.auth import get_user_model
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, views
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from afisha.filters import EventFilter
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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = Event.afisha_objects.not_finished_user_afisha(user=user)
        return queryset.order_by("startAt")


class MonthAPIView(views.APIView):
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        values_qs = (
            Event.afisha_objects.not_finished_user_afisha(user=user)
            .annotate(month_id=ExtractMonth("startAt"))
            .values_list("month_id", flat=True)
            .distinct()
        )

        list_of_months = [
            ({"id": month_id, "name": calendar.month_name[month_id]})
            for month_id in values_qs
        ]

        return JsonResponse(list_of_months, safe=False)
