from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_admin and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_admin and request.user.is_authenticated)


class IsJuridical(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and hasattr(request.user, 'juridical_user'))


class CurrentUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.pk == user.pk


class IsAuthenticatedAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.user == request.user
        return False
