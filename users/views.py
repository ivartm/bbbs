from rest_framework import generics
from users.models import Profile
from users.serializers import ProfileSerializer, TokenSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from users.utils import get_tokens_for_user


class TokenAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = get_tokens_for_user(user)
        return Response(token, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj
