from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from afisha.models import Event, EventParticipant
from afisha.serializers import EventSerializer
from common.models import City
from main.models import TEMP_DATA, Main
from main.serializers import MainSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.exceptions import CityNotSelected


class MainView(ListAPIView):
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)

    def get(self, request):
        context = {}
        if self.request.user.is_authenticated:
            city = self.request.user.profile.city
        else:
            if self.request.query_params.get("city") is None:
                raise CityNotSelected
            else:
                city, created = City.objects.get_or_create(
                    name=self.request.query_params.get("city")
                )
        event = Event.objects.filter(
            city=city, startAt__gt=timezone.now()
        ).first()
        event_participants = EventParticipant.objects.filter(event=event)
        booked = event_participants.filter(user_id=request.user.id)

        main_page = Main.objects.first()
        main_serializer = MainSerializer(
            main_page, context={"request": request}
        )
        event_serializer = EventSerializer(event, context={"request": request})
        context["event"] = {
            **event_serializer.data,
            "booked": booked.exists(),
            "takenSeats": event_participants.count(),
        }
        context.update(main_serializer.data)
        context.update(**TEMP_DATA)
        return Response(context)
