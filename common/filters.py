from rest_framework.generics import get_object_or_404
from common.models import City
from django_filters import rest_framework as filters

from common.exceptions import CityNotSelected
from places.models import Place, PlaceTag
from questions.models import Question, QuestionTag
from rights.models import Right, RightTag


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


class CityRequiredFilterBackend(filters.DjangoFilterBackend):
    """Requires city to filter. Takes it from user or query for anonimouses."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            city = request.user.profile.city
        else:
            city_id = request.query_params.get("city")
            if not city_id:
                raise CityNotSelected
            city = get_object_or_404(City, id=city_id)

        return queryset.filter(city=city)
