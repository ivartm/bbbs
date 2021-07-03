from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from common.filters import RightFilter
from rights.models import Right, RightTag
from rights.serializers import RightSerializer, RightTagSerializer


class RightTagList(generics.ListAPIView):
    queryset = RightTag.objects.all().order_by("id")
    serializer_class = RightTagSerializer


class RightViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Right.objects.all().prefetch_related("tags").order_by("id")
    serializer_class = RightSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RightFilter
