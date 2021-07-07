from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from afisha.models import Event, EventParticipant
from afisha.serializers import EventSerializer
from common.models import City
from main.models import Main
from main.serializers import MainSerializer


class MainView(ListAPIView):
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)

    def get(self, request):
        if self.request.user.is_authenticated:
            city = self.request.user.profile.city
        else:
            city, created = City.objects.get_or_create(name="Москва")

        main = Main.objects.first()
        event = Event.afisha_objects.not_started_city_afisha(city=city).first()
        booked = (
            request.user.is_authenticated
            and EventParticipant.objects.filter(
                event=event,
                user=request.user,
            ).exists()
        )
        if event:
            event.booked = booked

        main_serializer = MainSerializer(main, context={"request": request})
        event_serializer = EventSerializer(event, context={"request": request})

        context = {}
        context["event"] = {**event_serializer.data}
        context.update(main_serializer.data)
        # context.update(**TEMP_DATA)
        return Response(context)
