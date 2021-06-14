from django.contrib import admin

from .models import Place, PlaceTag
from users.utils import (
    AdminAndModerGenPermissionsMixin,
    AdminOnlyPermissionsMixin,
)


class PlaceAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "chosen",
        "age",
        "gender",
        "activity_type",
        "address",
        "link",
    )
    list_display_links = ("id", "title")
    filter_horizontal = ("tag",)
    list_filter = ("age", "gender", "activity_type")
    search_fields = ("title",)


class PlaceTagAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    pass


admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceTag, PlaceTagAdmin)
