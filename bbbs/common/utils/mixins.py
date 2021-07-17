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

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #
    #     return form

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[
            "text"
        ].initial = """Стандартная структура:

<подзаголовок>Введите ваш подзаголовок</подзаголовок>

<параграф>Введите ваш текст</параграф>


<подзаголовок>Подзаголовок для списка</подзаголовок>

<список>
<*>Элемент списка 1</*>
<*>Элемент списка 2</*>
</список>


<подзаголовок>Подзаголовок для текста</подзаголовок>

<параграф>Введите ваш текст</параграф>


<подзаголовок>Подзаголовок для карточки</подзаголовок>

<карточка>
Введите ваш текст,
который нужно поместить в цветную карточку
</карточка>
"""

        form.base_fields[
            "text"
        ].help_text = """
<pre>Между подзаголовком и текстовым тегом один перенос строки
Между текстовым тегом и следующим подзаголовком два переноса строки</pre>
<pre><h3>Используйте специальные теги:</h3>
<h3>
<подзаголовок> Тег для формирования подзаголовка в теле статьи&lt/подзаголовок>

<параграф> Тег для вывода стандартного форматированного текста&lt/параграф>

<список>
<*>
Тег "<список>" формирует таблицу,
а каждый ее элемент помещается в тег "<*>"
&lt/*>
&lt/список>

<карточка> Тег для вывода текста,
который нужно поместить в цветную карточку
&lt/карточка><h3></pre>

"""

        return form


class ConvertEditorTags:
    """
    Simple tag editor

    add in your serializer
        text = serializers.SerializerMethodField()


    """

    def get_text(self, obj):
        dict = {
            "<подзаголовок>": '<h2 class="section-title article__subtitle">',
            "</подзаголовок>": "</h2>",
            "<параграф>": '<p class="paragraph">',
            "</параграф>": "</p>",
            "<список>": '<ul class="card article__card">',
            "</список>": "</ul>",
            "<*>": '<li class="article__card-list-item">',
            "</*>": "</li>",
            "<карточка>": '<div class="card card_color_ article__card">'
            '<p class="paragraph">',
            "</карточка>": "</p></div>",
        }
        if obj.text != "":
            for key in dict:
                obj.text = obj.text.replace(key, dict[key])
        if '<div class="article__container">' not in obj.text:
            obj.text = '<div class="article__container"> \n' + obj.text
        if 'div class="card card_color_' in obj.text:
            color = obj.text.split('div class="card card_color_')
            color = color[1].split(" ")
            try:
                obj_color = obj.Colors(obj.color).name.lower()
                if obj_color and color[0]:
                    obj.text = obj.text.replace(color[0], obj_color)
                else:
                    obj.text = obj.text.replace(
                        'div class="card card_color_',
                        f'div class="card card_color_{obj_color}',
                    )
            except Exception:
                if not color[0]:
                    # если в админке нет поля color
                    # цвет карточки устанавливается по умолчанию желтый
                    obj.text = obj.text.replace(
                        'div class="card card_color_',
                        'div class="card card_color_yellow',
                    )
        return obj.text
