from rest_framework.permissions import SAFE_METHODS, BasePermission

# from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

EDIT_ACTIONS = ('update', 'partial_update', 'destroy')
