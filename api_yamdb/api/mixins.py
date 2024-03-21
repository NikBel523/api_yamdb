from rest_framework import exceptions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsReviewPatcherOrReadOnly, ManagesOnlyAdmin


class AdminManagebleMixin:
    permission_classes = (ManagesOnlyAdmin,)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role != 'admin':
            raise exceptions.PermissionDenied()

        raise exceptions.MethodNotAllowed(method='patch')

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='get')


class PaginationMixin:
    pagination_class = PageNumberPagination


class SearchMixin(PaginationMixin):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class AllowedMethodsMixin(PaginationMixin):
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')


class PatchRolesPermissionMixin(AllowedMethodsMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, IsReviewPatcherOrReadOnly)
