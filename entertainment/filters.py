from django_filters import rest_framework as filters

from entertainment.models import BookTag, VideoTag


class BookFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=BookTag.objects.all(),
        to_field_name="slug",
    )


class VideoFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=VideoTag.objects.all(),
        to_field_name="slug",
    )
