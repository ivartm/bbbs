from rest_framework import generics, status
from rest_framework.response import Response

from places.models import Place, PlaceTag
from places.serializers import (
    PlaceSerializerRead,
    PlaceSerializerWrite,
    PlaceTagSerializer,
)


class PlacesTagAPIView(generics.ListAPIView):
    queryset = PlaceTag.objects.all().order_by("name")
    serializer_class = PlaceTagSerializer


class PlacesAPIView(generics.ListCreateAPIView):
    queryset = Place.objects.all().prefetch_related("tag")
    serializer_class = PlaceSerializerRead

    def create(self, request, *args, **kwargs):
        serializer = PlaceSerializerWrite(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Success": "Спасибо! Мы приняли Вашу рекомендацию."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
