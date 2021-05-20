from django.contrib.admin import register
from django.contrib import admin

from afisha.models import Event, EventParticipant
from users.utils import StaffRequiredAdminMixin


@register(Event)
class EventAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = (
        "address",
        "contact",
        "title",
        "description",
        "start_at",
        "end_at",
        "seats",
        "taken_seats",
        "city",
    )
    empty_value_display = "-пусто-"

    def get_queryset(self, request):
        if request.user.profile.is_moderator_reg:
            return Event.objects.filter(city=request.user.profile.city)
        return Event.objects.all()

    def has_view_permission(self, request, obj=None):
        return request.user.profile.is_moderator_reg or request.user.profile.is_moderator_gen


@register(EventParticipant)
class EventParticipantAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("user", "event")
    empty_value_display = "-пусто-"
