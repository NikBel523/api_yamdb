from api.serializers import CategorySerializer, GenreSerializer
# from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, viewsets
from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from titles.models import Category, Genre


class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def partial_update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='patch')

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='get')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def partial_update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='patch')

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(method='get')
