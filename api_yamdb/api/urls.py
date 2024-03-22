from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ObtainTokenView,
    ReviewsViewSet,
    SingUpViewSet,
    TitleViewSet,
    UserProfileViewSet,
)

_v1_router = routers.DefaultRouter()

_v1_router.register('categories', CategoryViewSet, basename='categories')
_v1_router.register('genres', GenreViewSet, basename='genres')
_v1_router.register('titles', TitleViewSet, basename='titles')
_v1_router.register('users', UserProfileViewSet, basename='users')

_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews')
_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

_v1_paths = [
    path('', include(_v1_router.urls)),
    path(
        'auth/signup/', SingUpViewSet.as_view({'post': 'create'}),
        name='signup'),
    path(
        'auth/token/', ObtainTokenView.as_view(),
        name='token_obtain_pair'),
]

urlpatterns = [
    path('v1/', include(_v1_paths)),
]
