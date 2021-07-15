from django.contrib import admin
from django.contrib.admin import register

from bbbs.main.models import Main
from bbbs.users.utils import AdminOnlyPermissionsMixin

from .forms import MainAdminForm


@register(Main)
class MainAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    empty_value_display = "-пусто-"
    filter_horizontal = ("questions", "articles", "movies")
    form = MainAdminForm

    def has_add_permission(self, request):
        if Main.objects.first():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
