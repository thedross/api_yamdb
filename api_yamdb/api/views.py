from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.filters import TitleFilterSet
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
)
from api.permissions import (
    IsAuthorOrModeratorOrReadOnly,
    IsSuperOrAdminOrReadOnly
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
)


class BaseViewSet(mixins.CreateModelMixin,
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


class GenresViewSet(BaseViewSet):
    """
    Вью-сет моделей Genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(BaseViewSet):
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
    filter_backends = (DjangoFilterBackend, )
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = request.user
        title = self.get_current_title()
        headers = self.get_success_headers(serializer.validated_data)
        if not title.reviews.filter(author=author):
            serializer.save(
                author=author,
                title=title
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            "Вы уже написали отзыв к этому произведению.",
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_queryset(self):
        return self.get_current_title().reviews.all().order_by('-pub_date')


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
        return self.get_current_review().comments.all().order_by('-pub_date')
