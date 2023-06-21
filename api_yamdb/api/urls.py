from django.urls import include, path
from rest_framework.routers import DefaultRouter


from api.views import (
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
    CommentViewSet,
    ReviewViewSet,
)
from users.views import UsersViewSet, CreateUserView, TokenObtainView

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/', include([
        path('signup/', CreateUserView.as_view(), name='signup'),
        path('token/', TokenObtainView.as_view(), name='token')
    ])),
    path('v1/', include(router_v1.urls)),
]
