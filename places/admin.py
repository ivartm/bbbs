from django.contrib import admin

from .models import Place, PlaceTag


class PlaceAdmin(admin.ModelAdmin):
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


admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceTag)
