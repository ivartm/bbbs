from django.utils.translation import gettext_lazy as _
from users.models import Profile
from users.utils import StaffRequiredAdminMixin
from django.contrib.auth.models import User, Group

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ProfileInline(StaffRequiredAdminMixin, admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('role', 'city',)


class UserAdmin(StaffRequiredAdminMixin, UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('id', 'username',
                    'is_active', 'is_staff',
                    'user_role', 'user_city')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff',
                       'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def user_role(self, obj):
        return obj.profile.role

    def user_city(self, obj):
        return obj.profile.city


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
