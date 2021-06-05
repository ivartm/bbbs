from rest_framework import generics

from rights.models import Right
from rights.serializers import RightSerializer


class RightsList(generics.ListAPIView):
    queryset = Right.objects.all()
    serializer_class = RightSerializer
