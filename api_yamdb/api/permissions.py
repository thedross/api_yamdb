from rest_framework import permissions

"""
Для остальных случаев ставим пермишен на уровне проекта
или
IsAuthenticatesOrReadOnly, где необходимо
"""


class IsSuperOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешения для роли админ.
    Суперюзер - всегда админ, даже если изменить роль.
    """
    def has_permission(self, request, view):
        if view.basename in LIST_ONLY_VIEWS:
            return (
                view.action == 'list'
                or (request.user.is_authenticated and request.user.is_admin)
            )
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешения уровня модератор и автора.
    Автор может редактировать свой контент.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsSuperOrAdmin(permissions.BasePermission):
    """
    Разрешение уровня администратора и суперюзера.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
