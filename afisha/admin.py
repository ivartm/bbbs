from django.contrib import admin
from django.contrib.admin import register

from afisha.models import Event, EventParticipant
from users.utils import StaffRequiredAdminMixin


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "contact",
        "title",
        "description",
        "start_at",
        "end_at",
        "seats",
        "city",
    )
    empty_value_display = "-пусто-"

    def get_queryset(self, request):
        if request.user.profile.is_moderator_reg:
            return Event.objects.filter(city=request.user.profile.city)
        return Event.objects.all()

    # def get_readonly_fields(self, request, obj=None):
    #     # сделать поле адресс недоступным для редактирования для регионального модера
    #     # так же заполнить город автоматически. Присваивать город из профиля
    #     pass

    def has_add_permission(self, request):
        if request.user.is_anonymous:
            return False
        return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        return True

    def has_module_permission(self, request):
        if request.user.is_anonymous:
            return False
        return True


@register(EventParticipant)
class EventParticipantAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("user", "event")
    empty_value_display = "-пусто-"
