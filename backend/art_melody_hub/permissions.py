from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read-only access to anyone, write access to staff users only."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level: only the owner or staff can write. Read open."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None) or getattr(obj, 'master', None)
        return owner == request.user
