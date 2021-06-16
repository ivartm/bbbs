from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from places.models import Place, PlaceTag
from places.serializers import (
    PlaceSerializerRead,
    PlaceSerializerWrite,
    PlaceTagSerializer,
)


class PlacesTagList(ListAPIView):
    queryset = PlaceTag.objects.all().order_by("name")
    serializer_class = PlaceTagSerializer


class PlacesViewSet(ModelViewSet):
    queryset = Place.objects.all().prefetch_related("tag")
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        if self.action == "create":
            return PlaceSerializerWrite
        return PlaceSerializerRead
