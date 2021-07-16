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


class AdminEditor:
    """
    Mixin get help text with recommended tags
    """

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[
            "text"
        ].help_text = """
<pre><b><h1>Используйте специальные теги:</h1>
<h1><подзаголовок>Ваш подзаголовок&lt/подзаголовок>
<параграф>Ваш текст&lt/параграф>
<список>
<*>Элемент списка 1&lt/*>
<*>Элемент списка 2&lt/*>
&lt/список>
<карточка>Ваш текст&lt/карточка></h1></b></pre>"""
        return form


class ConvertEditorTags:
    """
    Simple tag editor
    """

    def save(self, *args, **kwargs):
        dict = {
            "<подзаголовок>": '<h2 class="section-title article__subtitle">',
            "</подзаголовок>": "</h2>",
            "<параграф>": '<p class="paragraph">',
            "</параграф>": "</p>",
            "<список>": '<ul class="card article__card">',
            "</список>": "</ul>",
            "<*>": '<li class="article__card-list-item">',
            "</*>": "</li>",
            "<карточка>": '<div class="card card_color_ article__card">',
            "</карточка>": "</div>",
        }
        if self.text != "":
            for key in dict:
                self.text = self.text.replace(key, dict[key])

        if 'div class="card card_color_' in self.text:
            color = self.text.split('div class="card card_color_')
            color = color[1].split(" ")
            try:
                obj_color = self.Colors(self.color).name.lower()
                if obj_color and color[0]:
                    self.text = self.text.replace(color[0], obj_color)
                else:
                    self.text = self.text.replace(
                        'div class="card card_color_',
                        f'<div class="card card_color_{obj_color}',
                    )
            except Exception:
                if not color[0]:
                    self.text = self.text.replace(
                        'div class="card card_color_',
                        'div class="card card_color_yellow',
                    )
        super().save(*args, **kwargs)
