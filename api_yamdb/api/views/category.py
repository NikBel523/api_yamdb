from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnly
from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class _BaseCategorizingView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    http_method_names = ('get', 'post', 'retrive', 'delete')
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(_BaseCategorizingView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(_BaseCategorizingView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
