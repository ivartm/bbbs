from django.contrib import admin

from story.models import Story, StoryImage
from users.utils import AdminAndModerGenPermissionsMixin


class StoryImagesInline(admin.StackedInline):
    model = StoryImage
    extra = 1


class StoryAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ["title", "prolog", "beginningOfFriendship"]
    list_filter = [
        "beginningOfFriendship",
    ]
    search_fields = [
        "title",
    ]
    ordering = [
        "-beginningOfFriendship",
    ]
    inlines = [StoryImagesInline]


admin.site.register(Story, StoryAdmin)
