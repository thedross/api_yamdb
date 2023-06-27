from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    permissions,
    viewsets,
)
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilterSet
from api.mixins import CreateListDestroyViewSet
from api.permissions import (
    IsAuthorOrModeratorOrReadOnly,
    IsSuperOrAdminOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
)


class GenresViewSet(CreateListDestroyViewSet):
    """
    Вью-сет моделей Genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(CreateListDestroyViewSet):
    """
    Вью-сет моделей Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Вью-сет моделей Title.
    """
    queryset = Title.objects.all().select_related(
        'category'
    ).prefetch_related(
        'genre'
    ).order_by(
        'name'
    ).annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('year', 'name', 'category')
    filterset_class = TitleFilterSet
    pagination_class = PageNumberPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperOrAdminOrReadOnly
    )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вью-сет моделей Review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrReadOnly
    ]
    default_ordering = '-pub_date'

    def get_current_title(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_current_title()
        )

    def get_queryset(self):
        return self.get_current_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вью-сет моделей Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrReadOnly
    ]
    default_ordering = '-pub_date'

    def get_current_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_current_review()
        )

    def get_queryset(self):
        return self.get_current_review().comments.all()
