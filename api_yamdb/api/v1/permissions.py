from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_admin))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or ((request.user.is_authenticated)
                    and request.user.is_admin))
# and (request.user.is_superuser or request.user.is_admin)))


class OwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_moderator or request.user.is_admin
                 or obj.author == request.user))
