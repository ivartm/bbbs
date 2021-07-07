from django.contrib import admin
from django.utils.html import format_html

from places.models import Place, PlaceTag
from users.utils import (
    AdminAndModerGenPermissionsMixin,
    AdminOnlyPermissionsMixin,
)


class PlaceAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
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
