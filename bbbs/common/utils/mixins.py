from django.contrib import admin
from django.utils.html import format_html


class AdminPreview:

    """
    Mixin makes preview for uploaded images

    Add this fields in admin class

        list_display = ("image_list_preview",)
        readonly_fields = ("image_change_preview",)

    """

    def image_change_preview(self, obj):
        if obj.image_url:
            if "https://" in obj.image_url:
                url = obj.image_url
            else:
                url = obj.image_url.url
            return format_html(
                '<img src="{}" width="600" height="300" style="'
                "border: 2px solid grey;"
                'border-radius:50px;" />'.format(url)
            )
        pass

    image_change_preview.short_description = "Превью"

    def image_list_preview(self, obj):
        if obj.image_url:
            if "https://" in obj.image_url:
                url = obj.image_url
            else:
                url = obj.image_url.url
            return format_html(
                '<img src="{}" width="100" height="50" style="'
                "border: 1px solid grey;"
                'border-radius:10px;" />'.format(url)
            )
        pass

    image_list_preview.short_description = "Картинка"


class AdminColor:

    """
    Mixin makes colored circles from the colors used in the object

    Add this field in admin class

        list_display = ("colored_circle",)

    """

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


class AdminAutoSlugHelpText:

    """
    This mixin adds the hint text when editing slug
    """

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            if kwargs["fields"]:
                form.base_fields[
                    "slug"
                ].help_text = """
                    Будьте внимательны! Slug автоматически заполняется только
                    при создании тэга. Во время редактирования пожалуйста
                    введите вручную.
                    """
        return form
