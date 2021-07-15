from django.contrib import admin

from bbbs.story.models import Story, StoryImage
from bbbs.users.utils import AdminAndModerGenPermissionsMixin


class StoryImagesInline(admin.StackedInline):
    model = StoryImage
    extra = 1


class StoryAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ["title", "prolog", "beginning_of_friendship"]
    list_filter = [
        "beginning_of_friendship",
    ]
    search_fields = [
        "title",
    ]
    ordering = [
        "-beginning_of_friendship",
    ]
    inlines = [StoryImagesInline]


admin.site.register(Story, StoryAdmin)
