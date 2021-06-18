from django_filters import rest_framework as filters

from .models import Right, RightTag


class RightFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=RightTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Right
        fields = ["tags"]
