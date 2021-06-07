from django.contrib import admin
from django.contrib.admin import register

from questions.models import Question, Tag
from users.utils import StaffRequiredAdminMixin


@register(Question)
class QuestionAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("question", "answer", "pubDate")
    list_filter = ("tag", "pubDate")
    search_fields = ("question",)
    empty_value_display = "Без тегов"


@register(Tag)
class TagAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
