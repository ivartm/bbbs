from django.utils.translation import gettext_lazy as _

from users.mixins import DynamicLookupMixin
from users.models import Profile
from users.utils import StaffRequiredAdminMixin
from django.contrib.auth.models import User, Group

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ProfileInline(StaffRequiredAdminMixin, admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    fields = (
        "role",
        "city",
    )


class UserAdmin(StaffRequiredAdminMixin, DynamicLookupMixin, UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "id",
        "username",
        "is_active",
        "is_staff",
        "profile__role",
        "profile__city",
    )
    list_filter = (
        "is_active",
        "profile__role",
        "profile__city",
    )
    profile__role_short_description = "роль"
    profile__city_short_description = "город"
    list_display_links = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_fieldsets(self, request, obj=None):
        if not (request.user.is_superuser or request.user.profile.is_admin):
            fieldsets = (
                (None, {"fields": ("username",)}),
                (_("Personal info"), {"fields": ("email",)}),
            )
            return fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[
            "username"
        ].help_text = "В качестве имени укажите email пользователя"
        return form

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def user_role(self, obj):
        return obj.profile.role

    def user_city(self, obj):
        return obj.profile.city


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
