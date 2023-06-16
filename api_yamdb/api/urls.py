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
