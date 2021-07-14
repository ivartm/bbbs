from django.contrib import admin

from common.utils.mixins import AdminColor, AdminPreview
from rights.models import Right, RightTag
from users.utils import AdminAndModerGenPermissionsMixin


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


class RightTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
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
