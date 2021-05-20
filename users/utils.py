class StaffRequiredAdminMixin(object):

    def check_perm(self, user_obj):
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
        if request.user.profile.is_moderator_gen:
            return True
        return self.check_perm(request.user)

    def has_module_permission(self, request):
        return True
