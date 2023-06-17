from django.urls import include, path
from rest_framework import routers

from api.views import (
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
)

app_name = 'api'

router_apiv1 = routers.DefaultRouter()
router_apiv1.register(r'titles', TitlesViewSet, basename='titles')
router_apiv1.register(r'genres', GenresViewSet, basename='genres')
router_apiv1.register(r'categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_apiv1.urls)),
]
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
    basename='comment'
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
