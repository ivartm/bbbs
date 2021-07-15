from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

from bbbs.users.mixins import DynamicLookupMixin
from bbbs.users.models import Curator, Profile
from bbbs.users.utils import (
    AdminAndModerGenPermissionsMixin,
    AdminOnlyPermissionsMixin,
)


class ProfileInline(AdminAndModerGenPermissionsMixin, admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    filter_horizontal = ("region",)
    fields = (
        "role",
        "city",
        "region",
        "curator",
    )

    def get_fields(self, request, obj=None):
        if obj.profile.is_moderator_reg:
            return ["role", "city", "region"]
        elif obj.profile.is_mentor:
            return ["role", "city", "curator"]
        return ["role", "city", "curator"]


class UserAdmin(AdminOnlyPermissionsMixin, DynamicLookupMixin, UserAdmin):
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
    list_select_related = (
        "profile",
        "profile__city",
    )
    profile__role_short_description = "роль"
    profile__city_short_description = "город"
    list_display_links = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
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
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return "is_superuser"

    def get_fieldsets(self, request, obj=None):
        if request.user.profile.is_moderator_gen:
            fieldsets = (
                (None, {"fields": ("username", "email")}),
                (_("Personal info"), {"fields": ("first_name", "last_name")}),
                (
                    _("Permissions"),
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                        )
                    },
                ),
            )
            return fieldsets
        return super().get_fieldsets(request, obj)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def user_role(self, obj):
        return obj.profile.role

    def user_city(self, obj):
        return obj.profile.city

    def has_view_permission(self, request, obj=None):
        if not request.user.is_anonymous:
            return (
                request.user.profile.is_admin
                or request.user.profile.is_moderator_gen
            )
        return False


class CuratorAdmin(AdminOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = [
        "last_name",
        "first_name",
        "gender",
        "email",
    ]
    search_fields = [
        "last_name",
        "email",
    ]


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Curator, CuratorAdmin)
