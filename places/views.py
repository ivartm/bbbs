from rest_framework.generics import ListCreateAPIView

from .models import Place
from .serializers import PlaceSerializer


class PlaceList(ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
