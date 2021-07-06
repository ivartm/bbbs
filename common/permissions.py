from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            return obj.user == request.user
        return False
