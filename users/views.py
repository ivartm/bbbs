from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import Profile
from users.serializers import ProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj
