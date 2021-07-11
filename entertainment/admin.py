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


class MovieAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class VideoTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class VideoAdmin(
    AdminAndModerGenPermissionsMixin, AdminPreview, admin.ModelAdmin
):
    list_display = ["title", "author", "pubDate", "image_list_preview"]
    readonly_fields = ("image_change_preview", "duration")
    filter_horizontal = ("tags",)

    def change_view(self, request, object_id, extra_context=None):
        self.exclude = ("creative_url",)
        return super(VideoAdmin, self).change_view(
            request, object_id, extra_context
        )

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
            "imageUrl"
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
        "isMain",
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
