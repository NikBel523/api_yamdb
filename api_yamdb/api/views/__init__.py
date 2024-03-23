from .category import CategoryViewSet, GenreViewSet
from .review import CommentViewSet, ReviewsViewSet
from .title import TitleViewSet
from .user import ObtainTokenView, SignupView
from .user_profile import UserProfileViewSet

__all__ = [
    CategoryViewSet,
    GenreViewSet,
    ReviewsViewSet,
    CommentViewSet,
    TitleViewSet,
    SignupView,
    ObtainTokenView,
    UserProfileViewSet]
