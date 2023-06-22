from rest_framework import permissions

"""
Для остальных случаев ставим пермишен на уровне проекта
или
IsAuthenticatesOrReadOnly, где необходимо
"""

LIST_ONLY_VIEWS = ('categories', 'genres')


class IsSuperOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Разрешения для роли админ.
    Суперюзер - всегда админ, даже если изменить роль.
    """
    def has_permission(self, request, view):
        if view.basename in LIST_ONLY_VIEWS:
            return (
                view.action == 'list'
                or request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            or (request.user.is_admin or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAuthorOrModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Разрешения уровня модератор и автора.
    Автор может редактировать свой контент.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
        )
