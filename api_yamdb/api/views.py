from rest_framework import (
    filters,
    permissions,
    viewsets,
)
from rest_framework.pagination import PageNumberPagination

from titles.models import (
    Title,
    Genre,
    Category,
    Review,
    Comment,
)
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет для GenresViewSet и CategoriesViewSet."""
    permission_classes = (
        IsAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class GenresViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().select_related(
        'category'
    ).prefetch_related(
        'genre'
    )
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
