from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
    CommentViewSet,
    ReviewViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(
    r'^titels/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'^titels/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
