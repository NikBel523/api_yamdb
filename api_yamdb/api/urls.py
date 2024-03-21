from django.urls import include, path
from rest_framework import routers

from api.views.category import CategoryViewSet, GenreViewSet
from api.views.review import CommentViewSet, ReviewsViewSet
from api.views.title import TitleViewSet
from api.views.user import AuthViewSet, UserViewSet
from api.views.user_profile import UserProfileViewSet

v1_router = routers.DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users', UserProfileViewSet, basename='users')
# TODO нужно применить DRY? воможно через NestedSimpleRouter
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/',
         UserViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/', AuthViewSet.as_view({'post': 'create'})),
]
