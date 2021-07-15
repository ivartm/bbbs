from django.contrib import admin

from bbbs.users.utils import (
    AdminAndModerGenPermissionsMixin,
    AdminOnlyPermissionsMixin,
)

from .models import City, Meeting


class CityAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ("id", "name", "is_primary")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("is_primary",)
    empty_field = "--- пусто ---"


class MeetingAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ("date", "image", "smile", "place")


admin.site.register(City, CityAdmin)
admin.site.register(Meeting, MeetingAdmin)
