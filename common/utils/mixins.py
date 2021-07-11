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
                '<img src="{}" width="600" height="300" />'.format(url)
            )

    image_change_preview.short_description = "Превью"

    def image_list_preview(self, obj):
        if obj.image_url:
            if "https://" in obj.image_url:
                url = obj.image_url
            else:
                url = obj.image_url.url
            return format_html(
                '<img src="{}" width="100" height="50" />'.format(url)
            )

    image_list_preview.short_description = "Картинка"
