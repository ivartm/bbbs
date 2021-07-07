from django.conf import settings
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profile
from users.serializers import (
    ProfileSerializerRead,
    ProfileSerializerWrite,
    TokenSerializer,
)
from users.utils import get_tokens_for_user

EMAIL_RESET_PASSWORD_TEMPLATE_ID = settings.EMAIL_RESET_PASSWORD_TEMPLATE_ID


class TokenAPI(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(methods=["post"], request_body=TokenSerializer)
    @action(detail=False, methods=["post"])
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = get_tokens_for_user(user)
        return Response(token, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializerWrite

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

    def get(self, *args):
        queryset = self.get_object()
        serializer = ProfileSerializerRead(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        client = self.get_object()
        serializer = ProfileSerializerWrite(
            client, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            serializer = ProfileSerializerRead(client)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            data="Неверные данные", status=status.HTTP_400_BAD_REQUEST
        )


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    base_url = instance.request.build_absolute_uri(
        reverse("password_reset:reset-password-confirm")
    )
    email = reset_password_token.user.email
    key = reset_password_token.key
    link = f"{base_url}?token={key}"

    message = EmailMessage(to=[email])
    message.template_id = EMAIL_RESET_PASSWORD_TEMPLATE_ID
    message.merge_data = {
        email: {"link": link},
    }
    message.send()
