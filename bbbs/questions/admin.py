from django.contrib import admin

from bbbs.questions.models import Question, QuestionTag
from bbbs.users.utils import AdminAndModerGenPermissionsMixin


class QuestionAdmin(AdminAndModerGenPermissionsMixin, admin.ModelAdmin):
    list_display = [
        "question",
        "answer",
        "pub_date",
    ]
    list_filter = [
        "tags",
        "pub_date",
    ]
    search_fields = [
        "question",
    ]
    filter_horizontal = ["tags"]
    ordering = [
        "answer",
        "-pub_date",
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
    ordering = ["name"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionTag, QuestionTagAdmin)
