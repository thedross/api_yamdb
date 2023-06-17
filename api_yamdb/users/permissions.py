from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsSuperOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Разрешения для роли админ.
    Суперюзер - всегда админ, даже если изменить роль.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (obj == request.user or request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Разрешение для роли админ."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthorOrModeratorOrReadOnly(BasePermission):
    """Разрешения для роли модератор"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
        )    