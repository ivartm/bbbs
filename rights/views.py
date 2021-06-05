from rest_framework.generics import ListAPIView

from rights.models import Right
from rights.serializers import RightSerializer


class RightList(ListAPIView):
    queryset = Right.objects.all()
    serializer_class = RightSerializer
