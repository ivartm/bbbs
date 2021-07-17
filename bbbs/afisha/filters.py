from django.contrib import admin
from django_filters import rest_framework as filters

from bbbs.common.models import City


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class CitySelectFilter(admin.SimpleListFilter):
    title = "Города"
    parameter_name = "city_name"

    def lookups(self, request, model_admin):
        if request.user.profile.is_moderator_reg:
            queryset = City.objects.filter(region=request.user.profile)
        else:
            queryset = City.objects.all()
        values_qs = queryset.values_list("id", "name").order_by("name")
        return values_qs

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city_id=self.value())
        return queryset


class EventFilter(filters.FilterSet):
    month = NumberInFilter(
        field_name="start_at__month",
        lookup_expr="in",
    )
