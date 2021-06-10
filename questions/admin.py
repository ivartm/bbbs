from django.contrib import admin
from django.contrib.admin import register

from questions.models import Question, QuestionTag
from users.utils import StaffRequiredAdminMixin


@register(Question)
class QuestionAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("question", "answer", "pubDate")
    list_filter = ("tag", "pubDate")
    search_fields = ("question",)
    empty_value_display = "Без тегов"
    ordering = ("answer", "-pubDate")


@register(QuestionTag)
class TagAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    ordering = ("name",)
