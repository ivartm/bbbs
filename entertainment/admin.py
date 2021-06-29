from django.contrib import admin
from django.utils.html import format_html

from users.utils import AdminAndModerGenPermissionsMixin

from entertainment.models import (
    Guide,
    MovieTag,
    Movie,
    VideoTag,
    Video,
    BookTag,
    Book,
    Article,
)


class GuideAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "image_list_preview",
    ]
    readonly_fields = ("image_change_preview",)
    list_display_links = ("id", "title")
    search_fields = ("title", "description")

    def image_change_preview(self, obj):
        if obj.imageUrl:
            return format_html(
                '<img src="{}" width="600" height="300" />'.format(
                    obj.imageUrl.url
                )
            )

    image_change_preview.short_description = "Превью"

    def image_list_preview(self, obj):
        if obj.imageUrl:
            return format_html(
                '<img src="{}" width="100" height="50" />'.format(
                    obj.imageUrl.url
                )
            )

    image_list_preview.short_description = "Картинка"


class MovieTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class MovieAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class VideoTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class VideoAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class BookTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class BookAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


class ArticleAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    pass


admin.site.register(Guide, GuideAdmin)
admin.site.register(MovieTag, MovieTagAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(VideoTag, VideoTagAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(BookTag, BookTagAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Article, ArticleAdmin)
