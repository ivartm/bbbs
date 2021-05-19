from rest_framework import generics
from django.contrib.auth.models import User
from users.models import Profile
from users.serializers import ProfileSerializer, TokenSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class TokenAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data['username'])
        token = get_tokens_for_user(user)
        return Response(
            token, status=status.HTTP_201_CREATED
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(user=self.request.user)
        return obj
