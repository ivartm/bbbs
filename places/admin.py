from django.contrib import admin
from django.utils.html import format_html

from users.utils import (
    AdminAndModerGenPermissionsMixin,
    AdminOnlyPermissionsMixin,
)

from places.models import Place, PlaceTag


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
        "image_list_preview",
    )
    readonly_fields = ("image_change_preview",)
    list_display_links = ("id", "title")
    filter_horizontal = ("tags",)
    list_filter = ("age", "gender", "activity_type")
    search_fields = ("title",)

    def image_change_preview(self, obj):
        if obj.imageUrl:
            return format_html(
                '<img src="{}" width="600" height="300" />'.format(
                    obj.imageUrl.url
                )
            )

    image_change_preview.short_description = "Превью"

    def image_list_preview(self, obj):
        if obj.imageUrl:
            return format_html(
                '<img src="{}" width="100" height="50" />'.format(
                    obj.imageUrl.url
                )
            )

    image_list_preview.short_description = "Картинка"


class PlaceTagAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
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
