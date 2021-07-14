from django_filters import rest_framework as filters

from common.exceptions import CityNotSelected
from common.models import City
from places.models import Place, PlaceTag


class PlaceFilter(filters.FilterSet):
    """By tags, age and city filter with request inspecting logic.

    On a request basis the filter do:
        - if the user is authenticated it returns queryset filtered by the
        user's city
        - if the user is UNauthenticated it requires 'city' query param
        - could be filtered by tags
        - could be filtered by age with 'gte' or 'lte' kyewords
        (age__gte=10 means return all places with age greeter(>) or = 10)

        If an authenticated user passes 'city' query param that is different
        from the user's city it returns zero results. It's expected behavior.
    """

    city = filters.ModelChoiceFilter(queryset=City.objects.all())
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=PlaceTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Place
        fields = {
            "age": ["gte", "lte"],
        }

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


class PlaceTagFilter(filters.FilterSet):
    """List of PlaceTags that used for 'place' objects in user's city.

    On a request basis the filter do:
        - if the user is authenticated it returns queryset filtered by the
        user's city.
        - if the user is UNauthenticated it requires 'city' query param

        If an authenticated user passes 'city' query param that is different
        from the user's city it returns zero results. It's expected behavior.
    """

    city = filters.ModelChoiceFilter(
        field_name="places__city",
        queryset=City.objects.all(),
    )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, "user", None)
        if user.is_authenticated:
            city = user.profile.city
            return parent.filter(places__city=city).distinct()
        city_id = self.request.query_params.get("city", None)
        if not city_id:
            raise CityNotSelected
        return parent
