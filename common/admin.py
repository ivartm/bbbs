from django.contrib import admin

from users.utils import AdminOnlyPermissionsMixin

from .models import City, Meeting


class CityAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ("id", "name", "isPrimary")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("isPrimary",)
    empty_field = "--- пусто ---"


class MeetingAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ("date", "image", "smile", "place")


admin.site.register(City, CityAdmin)
admin.site.register(Meeting, MeetingAdmin)
