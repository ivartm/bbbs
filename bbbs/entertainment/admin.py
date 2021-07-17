from django.contrib import admin

from bbbs.common.utils.mixins import AdminColor, AdminEditor, AdminPreview
from bbbs.entertainment.models import (
    Article,
    Book,
    BookTag,
    Guide,
    Movie,
    MovieTag,
    Video,
    VideoTag,
)
from bbbs.users.utils import AdminAndModerGenPermissionsMixin


class GuideAdmin(
    AdminAndModerGenPermissionsMixin,
    AdminPreview,
    AdminEditor,
    admin.ModelAdmin,
):
    list_display = [
        "id",
        "title",
        "description",
        "image_list_preview",
    ]
    readonly_fields = ("image_change_preview",)
    list_display_links = ("id", "title")
    search_fields = ("title", "description")


class MovieTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["name"],
    }


class MovieAdmin(
    AdminAndModerGenPermissionsMixin, AdminPreview, admin.ModelAdmin
):
    list_display = (
        "id",
        "title",
        "image_list_preview",
    )
    readonly_fields = (
        "image_change_preview",
        "duration",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[
            "title"
        ].help_text = "Если поле пустое - сохранится название с youtube"
        form.base_fields[
            "producer"
        ].help_text = "Если поле пустое - сохранится автор с youtube"
        form.base_fields[
            "image_url"
        ].help_text = "Если поле пустое - сохранится превью с youtube"
        form.base_fields[
            "description"
        ].help_text = "Если поле пустое - сохранится описание с youtube"
        form.base_fields[
            "year"
        ].help_text = "Если поле пустое - сохранится превью с youtube"
        return form


class VideoTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["name"],
    }


class VideoAdmin(
    AdminAndModerGenPermissionsMixin, AdminPreview, admin.ModelAdmin
):
    list_display = ["title", "author", "pub_date", "image_list_preview"]
    readonly_fields = ("image_change_preview", "duration")
    filter_horizontal = ("tags",)
    exclude = ("creative_url",)

    # def change_view(self, request, object_id, extra_context=None):
    #     self.exclude = ("creative_url",)
    #     return super(VideoAdmin, self).change_view(
    #         request, object_id, extra_context
    #     )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.profile.is_moderator_reg:
            form.base_fields["city"].queryset = request.user.profile.region
        form.base_fields[
            "title"
        ].help_text = "Если поле пустое - сохранится название с youtube"
        form.base_fields[
            "author"
        ].help_text = "Если поле пустое - сохранится автор с youtube"
        form.base_fields[
            "image_url"
        ].help_text = "Если поле пустое - сохранится превью с youtube"
        return form


class BookTagAdmin(
    AdminAndModerGenPermissionsMixin, AdminColor, admin.ModelAdmin
):
    list_display = ("name", "colored_circle")
    prepopulated_fields = {
        "slug": ["name"],
    }


class BookAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ("id", "tag", "title", "author")


class ArticleAdmin(
    AdminAndModerGenPermissionsMixin,
    AdminPreview,
    AdminColor,
    AdminEditor,
    admin.ModelAdmin,
):
    list_display = (
        "id",
        "title",
        "is_main",
        "colored_circle",
        "image_list_preview",
    )
    readonly_fields = ("image_change_preview",)


admin.site.register(Guide, GuideAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(VideoTag, VideoTagAdmin)
admin.site.register(MovieTag, MovieTagAdmin)
admin.site.register(BookTag, BookTagAdmin)
