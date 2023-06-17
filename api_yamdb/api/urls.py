from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    ReviewViewSet,
)

router_v1 = DefaultRouter()

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
    path(
        'v1/',
        include(router_v1.urls)
    ),
]
