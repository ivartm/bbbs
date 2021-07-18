from django.contrib import admin

from bbbs.users.utils import AdminAndModerGenPermissionsMixin

from .models import City


class CityAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ("id", "name", "is_primary")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("is_primary",)


admin.site.register(City, CityAdmin)
