from django_filters import rest_framework as filters
from django_filters.widgets import CSVWidget

from rights.models import RightTag


class RightFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=RightTag.objects.all(),
        to_field_name="slug",
        widget=CSVWidget(),
    )
