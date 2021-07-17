from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bbbs.places.filters import PlaceFilter, PlaceTagFilter
from bbbs.places.models import Place, PlaceTag
from bbbs.places.serializers import PlaceSerializer, PlaceTagSerializer


class PlacesTagAPIView(ListAPIView):
    """Retruns tags that used for 'places' objects in specific city.

    The PlaceTagFilter uses user's profile.city to filter result by the city.
    If user is unauthenticated the 'city' query param is required.
    """

    queryset = PlaceTag.objects.exclude(places=None).distinct().order_by("id")
    serializer_class = PlaceTagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceTagFilter


class PlacesViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    """Retrun city's places.

    The PlaceFilter uses user's profile.city to filter result by the city.
    If user is unauthenticated the 'city' query param is required.
    It also could be filtered by tags, but it's not required.
    """

    queryset = (
        Place.objects.filter(published=True)
        .prefetch_related("tags")
        .order_by("-pub_date")
    )
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlaceFilter

    @action(
        methods=["get"],
        detail=False,
        url_path="main",
        url_name="main",
    )
    def get_main_place(self, request):
        """Returns 'place' obj for main position for user or city.

        1. If there are places with 'chosen' attr returns the last one
        2. If there is no places with 'chosen' attr returns last city's place
        3. If there is no places at all returns empty list
        """
        queryset = self.get_queryset()
        filtered_qs = self.filter_queryset(queryset)
        main_place = (
            filtered_qs.filter(chosen=True).order_by("-pub_date").first()
        )
        if not main_place:
            main_place = filtered_qs.order_by("-pub_date").first()

        if not main_place:
            empty_list = []
            return Response(empty_list, status=status.HTTP_200_OK)

        serializer = PlaceSerializer(main_place)
        return Response(serializer.data, status=status.HTTP_200_OK)
