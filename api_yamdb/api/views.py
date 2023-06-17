from django.shortcuts import get_object_or_404
from rest_framework import (
    permissions,
    viewsets,
)
from rest_framework.pagination import PageNumberPagination

from titles.models import (
    Review,
    Title,
)
from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вью-сет моделей Review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = [PageNumberPagination]
    default_ordering = '-pub_date'

    # Функция для получение заданного произведения
    def get_current_title(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_current_title()
        )

    def get_queryset(self):
        return self.get_current_title().titles_review.all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вью-сет моделей Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = [PageNumberPagination]
    default_ordering = '-pub_date'

    # Функция для получение заданного отзыва
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
        return self.get_current_post().comments.all()
