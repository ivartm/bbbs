from django.contrib import admin

from rights.models import Right, RightTag
from users.utils import AdminAndModerMixin


class RightAdmin(admin.ModelAdmin, AdminAndModerMixin):
    list_display = [
        "title",
        "description",
        "colored_circle",
    ]
    list_filter = [
        "tag",
    ]
    search_fields = [
        "title",
        "description",
        "text",
    ]


class RightTagAdmin(admin.ModelAdmin, AdminAndModerMixin):
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
