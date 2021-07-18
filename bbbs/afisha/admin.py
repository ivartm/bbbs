from django.contrib import admin
from django.contrib.admin import register

from bbbs.afisha.filters import CitySelectFilter
from bbbs.afisha.models import Event, EventParticipant
from bbbs.common.models import City
from bbbs.users.utils import AdminAndModersPermissionsMixin


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 0
    verbose_name_plural = "Список участников"


@register(Event)
class EventAdmin(AdminAndModersPermissionsMixin, admin.ModelAdmin):
    inlines = [
        EventParticipantInline,
    ]
    list_display = (
        "id",
        "city",
        "address",
        "contact",
        "title",
        "description",
        "start_at",
        "end_at",
        "seats",
    )
    list_filter = (
        CitySelectFilter,
        "start_at",
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
            "start_at"
        ].help_text = "Время и дата указываются в формате местного времени"
        form.base_fields[
            "end_at"
        ].help_text = "Время и дата указываются в формате местного времени"
        return form


@register(EventParticipant)
class EventParticipantAdmin(AdminAndModersPermissionsMixin, admin.ModelAdmin):
    list_display = ("user", "event")

    empty_value_display = "-пусто-"
    list_select_related = (
        "user",
        "event",
    )
