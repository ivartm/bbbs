from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bbbs.places.filters import PlaceFilter, PlaceTagFilter
from bbbs.places.models import Place, PlaceTag
from bbbs.places.serializers import PlaceSerializer, PlaceTagSerializer


class PlacesTagAPIView(generics.ListAPIView):
    """Retruns tags that used for 'places' objects in specific city.

    The PlaceTagFilter uses user's profile.city to filter result by the city.
    If user is unauthenticated the 'city' query param is required.
    """

    queryset = PlaceTag.objects.exclude(places=None).distinct().order_by("id")
    serializer_class = PlaceTagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceTagFilter


class PlacesAPIView(generics.ListCreateAPIView):
    """Retrun city's places.

    The PlaceFilter uses user's profile.city to filter result by the city.
    If user is unauthenticated the 'city' query param is required.
    It also could be filtered by tags, but it's not required.
    """

    queryset = (
        Place.objects.filter(published=True)
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceFilter
