from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet

from bbbs.rights.filters import RightFilter
from bbbs.rights.models import Right, RightTag
from bbbs.rights.serializers import RightSerializer, RightTagSerializer


class RightTagList(generics.ListAPIView):
    queryset = RightTag.objects.exclude(rights=None).distinct().order_by("id")
    serializer_class = RightTagSerializer


class RightViewSet(ReadOnlyModelViewSet):
    queryset = Right.objects.all().prefetch_related("tags").order_by("id")
    serializer_class = RightSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RightFilter
