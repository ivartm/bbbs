from django.contrib import admin

from main.models import Main
from django.contrib.admin import register
from .forms import MainAdminForm
from users.utils import AdminOnlyPermissionsMixin


@register(Main)
class MainAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    empty_value_display = "-пусто-"
    filter_horizontal = ("questions",)
    form = MainAdminForm

    def has_add_permission(self, request):
        if Main.objects.first():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
