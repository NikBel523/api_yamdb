from rest_framework.permissions import SAFE_METHODS, BasePermission

MANAGE_METHODS = ('POST', 'DELETE')


class ManagesOnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == 'POST':
            return hasattr(user, 'role') and user.role == 'admin'

        return user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in MANAGE_METHODS:
            return hasattr(user, 'role') and user.role == 'admin'

        return user.is_authenticated or request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        if request.user.role == 'admin':
            return True
