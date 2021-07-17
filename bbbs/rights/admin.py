from django.contrib import admin

from bbbs.common.utils.mixins import (
    AdminAutoSlugHelpText,
    AdminColor,
    AdminPreview,
)
from bbbs.rights.models import Right, RightTag
from bbbs.users.utils import AdminAndModerGenPermissionsMixin


class RightAdmin(
    AdminAndModerGenPermissionsMixin,
    AdminPreview,
    AdminColor,
    admin.ModelAdmin,
):
    list_display = [
        "title",
        "description",
        "colored_circle",
        "image_list_preview",
    ]
    readonly_fields = ("image_change_preview",)
    list_filter = [
        "tags",
    ]
    search_fields = [
        "title",
        "description",
        "text",
    ]
    filter_horizontal = ("tags",)


class RightTagAdmin(
    AdminAndModerGenPermissionsMixin, AdminAutoSlugHelpText, admin.ModelAdmin
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


admin.site.register(Right, RightAdmin)
admin.site.register(RightTag, RightTagAdmin)
