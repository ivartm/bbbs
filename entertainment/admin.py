from django.contrib import admin

from common.utils.mixins import AdminPreview
from entertainment.models import (
    Article,
    Book,
    BookTag,
    Guide,
    Movie,
    MovieTag,
    Video,
    VideoTag,
)
from users.utils import AdminAndModerGenPermissionsMixin


class GuideAdmin(
    AdminAndModerGenPermissionsMixin, AdminPreview, admin.ModelAdmin
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
    pass


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
        "image_url",
    )

    def get_fields(self, request, obj=None):
        if obj is None:
            fields = [
                "tags",
                "link",
                "title",
                "producer",
                "year",
                "description",
                "duration",
            ]
            return fields
        return super().get_fields(request, obj)


class VideoTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


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


class BookTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class BookAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class ArticleAdmin(
    AdminAndModerGenPermissionsMixin, AdminPreview, admin.ModelAdmin
):
    list_display = (
        "id",
        "title",
        "is_main",
        "image_list_preview",
    )
    readonly_fields = ("image_change_preview",)


admin.site.register(Guide, GuideAdmin)
admin.site.register(MovieTag, MovieTagAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(VideoTag, VideoTagAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(BookTag, BookTagAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Article, ArticleAdmin)
