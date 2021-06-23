# from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet, ModelMultipleChoiceFilter
from rest_framework.filters import BaseFilterBackend
from questions.models import Question, QuestionTag


class QuestionFilter(FilterSet):
    tag = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=QuestionTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Question
        fields = ["tags"]


class CityAuthFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        if self.request.user.is_authenticated:
            city = self.request.user.profile.city
        else:
            city = self.request.query_params.get("city")
        return queryset.filter(city=city)
