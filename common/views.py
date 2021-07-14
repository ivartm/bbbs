from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from common.models import City, Meeting
from common.permissions import IsOwner
from common.serializers import (
    CitySerializer,
    MeetingMessageSerializer,
    MeetingSerializer,
)

EMAIL_MEETING_TEMPLATE_ID = settings.EMAIL_MEETING_TEMPLATE_ID


class CityAPIView(ListAPIView):
    queryset = City.objects.all().order_by("-isPrimary", "name")
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class MeetingViewSet(ModelViewSet):
    serializer_class = MeetingSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Meeting.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["post"],
        name="send_to_curator",
        permission_classes=[IsAuthenticated, IsOwner],
    )
    def send_to_curator(self, request):
        serializer = MeetingMessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            meeting = get_object_or_404(
                Meeting, id=request.data["id"], user=request.user
            )
            local_url = meeting.image.url
            absolute_url = request.build_absolute_uri(local_url)
            curator_email = meeting.user.profile.curator.email
            description = meeting.description

            message = EmailMessage(
                to=[curator_email],
                subject=f"Описание встречи: {meeting.place}, {meeting.date}",
            )
            message.template_id = EMAIL_MEETING_TEMPLATE_ID
            message.merge_data = {
                curator_email: {
                    "description": description,
                    "link_to_image": absolute_url,
                },
            }
            message.send()
            meeting.send_to_curator = True
            meeting.save()
            return JsonResponse({"success": "Ok"}, status=status.HTTP_200_OK)
