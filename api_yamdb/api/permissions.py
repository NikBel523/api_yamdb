from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        if user.is_authenticated:
            return hasattr(user, 'role') and user.role == 'admin'

        return False


class IsReviewPatcherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            obj.author == request.user or request.user.role
            in ('moderator', 'admin'))


class IsAdmin(BasePermission):
    def _is_admin(self, request):
        user = request.user
        if user.is_anonymous:
            return False

        if user.is_superuser:
            return True

        return hasattr(user, 'role') and user.role == 'admin'

    def _is_me(self, view):
        return not view.request.user.is_anonymous and view.kwargs.get(
            'username', None) == 'me'

    # избавиться от id_me не получится, так как у нас нет маршрута users/me
    # весь корень обслуживается одной вьюшкой
    # 'auth/signup/', SingUpViewSet.as_view({'post': 'create'})
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (self._is_admin(
            request) or self._is_me(view))
