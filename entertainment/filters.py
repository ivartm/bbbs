from django_filters import rest_framework as filters

from entertainment.models import BookTag


class BookFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=BookTag.objects.all(),
        to_field_name="slug",
    )
