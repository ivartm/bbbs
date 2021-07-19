from django.contrib import admin

from bbbs.common.utils.mixins import AdminAutoSlugHelpText, AdminPreview
from bbbs.places.models import Place, PlaceTag
from bbbs.users.utils import AdminAndModerGenPermissionsMixin


class PlaceAdmin(
    AdminAndModerGenPermissionsMixin, AdminPreview, admin.ModelAdmin
):
    list_display = (
        "id",
        "published",
        "title",
        "chosen",
        "age",
        "gender",
        "activity_type",
        "city",
        "address",
        "link",
        "image_list_preview",
    )
    readonly_fields = ("image_change_preview",)
    list_display_links = ("id", "title")
    filter_horizontal = ("tags",)
    list_filter = ("published", "age", "gender", "activity_type", "city")
    search_fields = ("title",)


class PlaceTagAdmin(
    AdminAutoSlugHelpText, AdminAndModerGenPermissionsMixin, admin.ModelAdmin
):
    list_display = [
        "name",
        "slug",
    ]
    search_fields = [
        "name",
        "slug",
    ]
    prepopulated_fields = {
        "slug": ["name"],
    }


admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceTag, PlaceTagAdmin)
