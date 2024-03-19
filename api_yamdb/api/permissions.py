from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    # IsAuthenticatedOrReadOnly
)

EDIT_ACTIONS = ('update', 'partial_update', 'destroy')

user = get_user_model()


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        if request.user.role == 'admin':
            return True
