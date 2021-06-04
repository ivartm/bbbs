from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from afisha.models import Event
from afisha.serializers import EventSerializer
from main.models import TEMP_DATA


class MainView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        context = {}
        if self.request.user.is_authenticated:
            city = self.request.user.profile.city
        else:
            city = request.GET["city"]
        event = Event.objects.filter(
            city=city, startAt__gt=timezone.now()
        ).first()
        event_serializer = EventSerializer(event, context={"request": request})
        context["event"] = {**event_serializer.data}
        context.update(**TEMP_DATA)
        return Response(context)
