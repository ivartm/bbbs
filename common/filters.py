from django_filters import rest_framework as filters
from questions.models import QuestionTag, Question
from rights.models import RightTag, Right
from places.models import PlaceTag, Place


class QuestionFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=QuestionTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Question
        fields = ["tags"]


class RightFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=RightTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Right
        fields = ["tag"]


class PlaceFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=PlaceTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Place
        fields = ["tag"]
