from django.contrib import admin
from django.contrib.admin import register

from questions.models import Question, QuestionTag
from users.utils import AdminOnlyPermissionsMixin


@register(Question)
class QuestionAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ("question", "answer", "pubDate")
    list_filter = ("tags", "pubDate")
    search_fields = ("question",)
    empty_value_display = "Без тегов"
    ordering = ("answer", "-pubDate")


@register(QuestionTag)
class TagAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)
