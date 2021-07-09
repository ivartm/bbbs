from django_filters import rest_framework as filters

from common.exceptions import CityNotSelected
from common.models import City
from places.models import PlaceTag


class CityRequiredFilterSet(filters.FilterSet):
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


class PlaceFilter(CityRequiredFilterSet):
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


class PlaceTagFilter(CityRequiredFilterSet):
    city = filters.ModelChoiceFilter(
        field_name="places__city",
        queryset=City.objects.all(),
    )
