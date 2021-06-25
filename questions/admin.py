from django.contrib import admin

from questions.models import Question, QuestionTag
from users.utils import AdminAndModerGenPermissionsMixin


class QuestionAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = ["question", "answer", "pubDate"]
    list_filter = [
        "tags",
        "pubDate",
    ]
    search_fields = [
        "question",
    ]
    filter_horizontal = ("tags",)
    ordering = [
        "answer",
        "-pubDate",
    ]


class QuestionTagAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]
    search_fields = [
        "name",
        "slug",
    ]
    prepopulated_fields = {
        "slug": ["name"],
    }
    ordering = ("name",)


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionTag, QuestionTagAdmin)
