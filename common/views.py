# from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import CharField, Value
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from petrovich.enums import Case
from petrovich.main import Petrovich
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from common.models import City, Meeting
from common.permissions import IsOwner
from common.serializers import (
    CitySerializer,
    MeetingMessageSerializer,
    MeetingSerializer,
    MyCitySerializer,
)
from users.models import Profile

# SEND_MEETING_TEMPLATE_ID = settings.SEND_MEETING_TEMPLATE_ID


class CityAPIView(ListAPIView):
    queryset = City.objects.all().order_by("-isPrimary", "name")
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class MyCityApiView(ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MyCitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Profile.objects.filter(user=user)
        return queryset


class MeetingAPIView(
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
    DestroyModelMixin,
    RetrieveModelMixin,
):
    serializer_class = MeetingSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.curator is not None:
            change_ending = Petrovich()
            name = (
                change_ending.firstname(
                    value=user.profile.curator.first_name,
                    case=Case.DATIVE,
                    # gender=user.profile.curator.gender,
                )
                + " "
                + user.profile.curator.last_name[0]
                + "."
            )
            queryset = Meeting.objects.filter(user=user).annotate(
                name=Value(name, output_field=CharField())
            )
        else:
            queryset = Meeting.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwner])
def send_meeting_to_curator(request):
    serializer = MeetingMessageSerializer(data=request.data)
    if serializer.is_valid():
        meeting = get_object_or_404(
            Meeting, id=request.data["id"], user=request.user
        )
        message = EmailMessage()
        message.subject = (
            f"Описание встречи: {meeting.place}, " f"{meeting.date}"
        )
        message.body = meeting.description
        message.to = [meeting.user.profile.curator.email]
        message.attach_file(meeting.image.path)
        # message.template_id = SEND_MEETING_TEMPLATE_ID
        message.send()
        meeting.send_to_curator = True
        meeting.save()
        return JsonResponse({"success": True}, status=status.HTTP_200_OK)
    else:
        return JsonResponse(
            {"success": False}, status=status.HTTP_400_BAD_REQUEST
        )
