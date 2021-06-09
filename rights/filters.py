from django_filters import rest_framework as filters

from .models import Right


class RightFilter(filters.FilterSet):
    tag = filters.CharFilter(
        field_name="tag",
        lookup_expr="slug",
    )

    class Meta:
        model = Right
        fields = ["tag"]
