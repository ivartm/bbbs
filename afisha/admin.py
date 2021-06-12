from django.contrib import admin
from django.contrib.admin import register

from afisha.filters import CitySelectFilter
from afisha.models import Event, EventParticipant
from common.models import City
from users.utils import StaffRequiredAdminMixin


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
        "address",
        "contact",
        "title",
        "description",
        "startAt",
        "endAt",
        "seats",
    )
    list_filter = (
        CitySelectFilter,
        "startAt",
    )
    empty_value_display = "-пусто-"
    search_fields = ("title",)

    def get_queryset(self, request):
        if request.user.profile.is_moderator_reg:
            return Event.objects.filter(
                city__in=City.objects.filter(region=request.user.profile)
            )

        else:
            return Event.objects.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.profile.is_moderator_reg:
            form.base_fields["city"].queryset = request.user.profile.region
        form.base_fields[
            "startAt"
        ].help_text = "Время и дата указываются в формате местного времени"
        form.base_fields[
            "endAt"
        ].help_text = "Время и дата указываются в формате местного времени"
        return form

    def has_add_permission(self, request):
        return not request.user.is_anonymous

    def has_view_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_change_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_module_permission(self, request):
        return not request.user.is_anonymous


@register(EventParticipant)
class EventParticipantAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("user", "event")
    empty_value_display = "-пусто-"
