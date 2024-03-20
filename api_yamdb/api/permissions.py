from rest_framework.permissions import SAFE_METHODS, BasePermission

MANAGE_METHODS = ('POST', 'DELETE', 'PATCH')


class ManagesOnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in MANAGE_METHODS:
            return hasattr(user, 'role') and user.role == 'admin'

        return user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in MANAGE_METHODS:
            return hasattr(user, 'role') and user.role == 'admin'

        return user.is_authenticated or request.method in SAFE_METHODS
