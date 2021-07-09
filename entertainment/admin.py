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


class VideoAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ("title", "author", "pub_date")


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
