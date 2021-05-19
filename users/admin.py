from django.utils.translation import gettext_lazy as _
from users.models import Profile
from django.contrib.auth.models import User, Group

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('role',)

    def has_change_permission(self, request, obj=None):
        is_admin = Profile.objects.get(user=request.user).is_admin
        is_superuser = request.user.is_superuser
        if is_superuser or is_admin:
            return True
        return False


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('pk', 'username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(UserAdmin, self).get_inline_instances(request, obj)

    # def has_delete_permission(self, request, obj=None):
    #     is_admin = Profile.objects.get(user=request.user).is_admin
    #     if not is_admin:
    #         return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        is_admin = Profile.objects.get(user=request.user).is_admin
        disabled_fields = set()

        if not (is_superuser or is_admin):
            disabled_fields |= {
                'is_staff',
                'is_active',
                'is_superuser',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
