from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на добавление и редактирование объекта только для администратора.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.is_admin is True
        )
