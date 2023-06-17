from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

"""
Для остальных случаев ставим пермишен на уровне проекта
или
IsAuthenticatesOrReadOnly, где необходимо
"""


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


class IsAuthorOrModeratorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Разрешения уровня модератор и автора.
    Автор может редактировать свой контент.
    """

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
