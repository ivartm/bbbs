from django_filters import rest_framework as filters
from rest_framework import generics

from rights.filters import RightFilter
from rights.models import Right, RightTag
from rights.serializers import RightSerializer, RightTagSerializer


class RightTagList(generics.ListAPIView):
    queryset = RightTag.objects.all()
    serializer_class = RightTagSerializer


class RightList(generics.ListAPIView):
    queryset = Right.objects.all().prefetch_related("tags")
    serializer_class = RightSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RightFilter
