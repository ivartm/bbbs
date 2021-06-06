from django.contrib import admin

from main.models import Main
from django.contrib.admin import register
from .forms import MainAdminForm


@register(Main)
class MainAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    filter_horizontal = ("questions",)
    form = MainAdminForm

    def has_add_permission(self, request):
        if Main.objects.first():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser or request.user.profile.is_admin:
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser or request.user.profile.is_admin:
            return True

    def has_module_permission(self, request):
        return True
