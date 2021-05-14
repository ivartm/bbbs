from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_admin:
            return True
