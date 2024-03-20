from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Title

from api.filters import TitleFilter
from api.permissions import ManagesOnlyAdmin, IsReviewPatcherOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class AdminManagebleMixin:
    permission_classes = (ManagesOnlyAdmin,)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role != 'admin':
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
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')
    permission_classes = (ManagesOnlyAdmin,)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')

    permission_classes = (IsAuthenticatedOrReadOnly, IsReviewPatcherOrReadOnly)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        # Добавляю .all() что бы певратить объект RelatedManager в QuerySet
        # Это обеспечивает работу пагинатора, который не может в RelatedManager
        # RelatedManager не работает для слайсов и индексации
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            # TODO заменить 'bingobongo' на self.request.user
            author=User.objects.get(username=self.request.user),
            title=self.get_title(),
        )
