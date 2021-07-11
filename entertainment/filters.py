from django_filters import rest_framework as filters

from entertainment.models import BookTag, MovieTag, VideoTag


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


class ArticleFilter(filters.FilterSet):
    isMain = filters.BooleanFilter(
        field_name="is_main",
        lookup_expr="icontains",
    )


class MovieFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=MovieTag.objects.all(),
        to_field_name="slug",
    )
