from django_filters import rest_framework as filters

from common.exceptions import CityNotSelected
from common.models import City
from entertainment.models import BookTag
from places.models import PlaceTag
from questions.models import QuestionTag
from rights.models import RightTag


class QuestionFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=QuestionTag.objects.all(),
        to_field_name="slug",
    )


class RightFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=RightTag.objects.all(),
        to_field_name="slug",
    )


class PlaceFilter(filters.FilterSet):
    """By tags and city filter with request inspecting logic.

    By request basis the filter do:
        - if user authenticated it returns queryset filtered by user's city.
        The filter doesn't require any query param but could be filtered by
        tags.

        - if user is UNauthenticated it requires 'city' query param

        If authenticated user pass 'city' query param that is different from
        user's city it returns zero result. It's expected behavior.
    """

    city = filters.ModelChoiceFilter(queryset=City.objects.all())
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=PlaceTag.objects.all(),
        to_field_name="slug",
    )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, "user", None)
        if user.is_authenticated:
            city = user.profile.city
            return parent.filter(city=city)
        city_id = self.request.query_params.get("city", None)
        if not city_id:
            raise CityNotSelected
        return parent


class BookFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=BookTag.objects.all(),
        to_field_name="slug",
    )
