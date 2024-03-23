from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return request.method in SAFE_METHODS or (
            user.is_authenticated and user.is_admin)


class IsReviewPatcherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.method in SAFE_METHODS or (
            obj.author == request.user or user.is_moderator or user.is_admin)


class IsAdmin(BasePermission):
    def _is_me(self, view):
        return not view.request.user.is_anonymous and view.kwargs.get(
            'username', '').casefold() == 'me'

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin
