from rest_framework import (
    permissions,
    viewsets,
)
from rest_framework.pagination import PageNumberPagination

from titles.models import (
    Review,
    Comment,
)
from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
