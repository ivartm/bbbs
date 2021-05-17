from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import City
from .serializers import CitySerializer


class CityAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
