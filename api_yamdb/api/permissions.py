from rest_framework.permissions import SAFE_METHODS, BasePermission

_MANAGE_METHODS = ('POST', 'DELETE', 'PATCH')


class ManagesOnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in _MANAGE_METHODS:
            return hasattr(user, 'role') and user.role == 'admin'

        return user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in _MANAGE_METHODS:
            return hasattr(user, 'role') and user.role == 'admin'

        return user.is_authenticated or request.method in SAFE_METHODS


class IsReviewPatcherOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (obj.author == request.user
                or request.user.role in ('moderator', 'admin'))


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

    def has_permission(self, request, view):
        return self._is_admin(request) or self._is_me(view)

    def has_object_permission(self, request, view, obj):
        return self._is_admin(request) or self._is_me(view)
