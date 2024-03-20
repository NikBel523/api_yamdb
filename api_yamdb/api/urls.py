from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewsViewSet,
    TitleViewSet,
)
from custom_auth.views import AuthViewSet, UserViewSet
from custom_auth.views2 import UserProfileViewSet

v1_router = routers.DefaultRouter()

"""
v1_router.register('auth', AuthViewSet, basename='auth')
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'title/(?P<title_id>\\d+)/reviews',
    ReviewsViewSet, basename='reviews')
v1_router.register(
    r'review/(?P<review_id>\\d+)/comments',
    CommentViewSet, basename='comments')
"""


v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users', UserProfileViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews')

"""
actionsMap = {
    "get": "retrieve",
    "post": "create",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy"}
"""

urlpatterns = [
    path('v1/', include(v1_router.urls)),

    path('v1/auth/signup/',
         UserViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/', AuthViewSet.as_view({'post': 'create'})),
    # path('v1/api-token-auth/', views.obtain_auth_token),
]
