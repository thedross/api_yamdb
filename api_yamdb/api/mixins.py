from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import IsSuperOrAdminOrReadOnly


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Базовый вьюсет для GenresViewSet и CategoriesViewSet.
    """
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperOrAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter, )
    pagination_class = PageNumberPagination
    search_fields = ('name', )
    lookup_field = 'slug'
