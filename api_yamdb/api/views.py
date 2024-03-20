from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, ManagesOnlyAdmin
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from titles.models import Category, Genre, Title


class AdminManagebleMixin:
    permission_classes = (ManagesOnlyAdmin,)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.role != 'admin':
                raise exceptions.PermissionDenied()

        raise exceptions.MethodNotAllowed(method='patch')

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='get')


class CategoryViewSet(AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    permission_classes = (IsAdminOrReadOnly,)
