from django.contrib import admin

from common.models import City


class CitySelectFilter(admin.SimpleListFilter):
    title = "Города"
    parameter_name = "city_name"

    def lookups(self, request, model_admin):
        list_of_cities = []
        if request.user.profile.is_moderator_reg:
            queryset = City.objects.filter(region=request.user.profile)
        else:
            queryset = City.objects.all()
        for city in queryset:
            list_of_cities.append((str(city.id), city.name))
        return sorted(list_of_cities, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city_id=self.value())
        return queryset
