from rest_framework import exceptions, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre

from api.permissions import ManagesOnlyAdmin
from api.serializers.category import CategorySerializer, GenreSerializer


class _AdminManagebleMixin:
    permission_classes = (ManagesOnlyAdmin,)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role != 'admin':
            raise exceptions.PermissionDenied()

        raise exceptions.MethodNotAllowed(method='patch')

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='get')


class CategoryViewSet(_AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(_AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
