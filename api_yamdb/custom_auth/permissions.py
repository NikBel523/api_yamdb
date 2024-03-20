from rest_framework.permissions import BasePermission


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
