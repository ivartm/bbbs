from django.contrib import admin
from users.utils import AdminOnlyPermissionsMixin

from .models import City


class CityAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ("id", "name", "isPrimary")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("isPrimary",)
    empty_field = "--- пусто ---"


admin.site.register(City, CityAdmin)
