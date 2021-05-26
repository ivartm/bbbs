from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from afisha.models import Event
from afisha.serializers import EventSerializer
from django.utils import timezone
from main.models import TEMP_DATA
from django.shortcuts import get_object_or_404


class MainView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        context = {}
        event = Event.objects.filter(start_at__gt=timezone.now()).first()
        # event = get_object_or_404(Event, start_at__gt=timezone.now())
        event_serializer = EventSerializer(event, context={'request': request})
        context['event'] = {**event_serializer.data}
        context.update(**TEMP_DATA)
        return Response(context)
