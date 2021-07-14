from django.contrib import admin
from django.utils.html import format_html

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
    filter_horizontal = ("tags",)

    @admin.display(
        description="Цвет фигуры",
    )
    def colored_circle(self, obj):
        return format_html(
            "<span style='"
            "height: 25px;"
            "width: 25px;"
            "border: 1px solid grey;"
            "border-radius: 50%;"
            "display: inline-block;"
            "background-color: {};'>"
            "</span>",
            obj.color,
        )


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
