from django.contrib import admin

from rights.models import Right, RightTag
from users.utils import AdminAndModerGenPermissionsMixin


class RightAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "colored_circle",
    ]
    list_filter = [
        "tags",
    ]
    search_fields = [
        "title",
        "description",
        "text",
    ]


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
