from rest_framework import exceptions, filters, viewsets

from api.permissions import AdminOrReadOnly
from api.serializers.category import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class _AdminManagebleMixin:
    permission_classes = (AdminOrReadOnly,)

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
    lookup_field = 'slug'


class GenreViewSet(_AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
