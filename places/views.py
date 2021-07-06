from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from common.filters import PlaceFilter
from places.models import Place, PlaceTag
from places.serializers import PlaceSerializer, PlaceTagSerializer


class PlacesTagAPIView(generics.ListAPIView):
    queryset = PlaceTag.objects.all().order_by("id")
    serializer_class = PlaceTagSerializer


class PlacesAPIView(generics.ListCreateAPIView):
    queryset = (
        Place.objects.filter(published=True)
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceFilter
