from rest_framework_simplejwt.tokens import RefreshToken


class StaffRequiredAdminMixin:

    def check_perm(self, user_obj):
        if user_obj.is_anonymous:
            return False
        if user_obj.profile.is_admin or user_obj.is_superuser:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_delete_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_view_permission(self, request, obj=None):
        if not request.user.is_anonymous:
            return request.user.profile.is_admin or\
                   request.user.profile.is_moderator_gen
        return self.check_perm(request.user)

    def has_module_permission(self, request):
        return True


class AdminAndModerMixin:

    def check_perm(self, user_obj):
        if user_obj.is_anonymous:
            return False
        if user_obj.profile.is_admin or user_obj.is_superuser or\
                user_obj.profile.is_moderator_gen:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_delete_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_view_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_module_permission(self, request):
        return True


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
