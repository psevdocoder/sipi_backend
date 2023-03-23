from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(IsAdmin):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or \
            request.user.is_authenticated and request.user.is_moderator


class IsBasicUser(IsModerator):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or \
            request.user.is_authenticated and request.user.is_basic_user


class IsAdminOrAuthRead(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
            (request.method in SAFE_METHODS or request.user.is_admin)


class IsModeratorOrAuthRead(IsAdminOrAuthRead):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) or
            request.user.is_authenticated and (
                request.user.is_moderator or
                request.method in SAFE_METHODS
            )
        )


class HasFilterQueryParam(BasePermission):
    def has_permission(self, request, view):
        return bool(request.query_params)
