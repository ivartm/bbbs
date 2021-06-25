from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from places.models import Place, PlaceTag
from places.serializers import (
    PlaceSerializer,
    PlaceTagSerializer,
)
from common.filters import PlaceFilter


class PlacesTagAPIView(generics.ListAPIView):
    queryset = PlaceTag.objects.all().order_by("name")
    serializer_class = PlaceTagSerializer


class PlacesAPIView(generics.ListCreateAPIView):
    queryset = Place.objects.all().prefetch_related("tags")
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PlaceFilter
