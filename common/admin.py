from django.contrib import admin

from users.utils import AdminAndModerGenPermissionsMixin

from .models import City


class CityAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ("id", "name", "isPrimary")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("isPrimary",)
    empty_field = "--- пусто ---"


admin.site.register(City, CityAdmin)
