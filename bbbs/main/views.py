from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from bbbs.afisha.models import Event
from bbbs.afisha.serializers import EventSerializer
from bbbs.main.models import Main
from bbbs.main.serializers import MainSerializer


class MainView(ListAPIView):
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)

    def get(self, request):
        context = {}
        user = request.user
        if user.is_authenticated:
            event = Event.afisha_objects.not_started_user_afisha(
                user=user
            ).first()
            event_serializer = EventSerializer(event)
            context["event"] = {**event_serializer.data}

        main = Main.objects.first()
        main_serializer = MainSerializer(main, context={"request": request})
        context.update(main_serializer.data)

        return Response(context)
