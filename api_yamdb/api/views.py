from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, viewsets
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, ManagesOnlyAdmin
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from titles.models import Category, Genre, Review, Title


User = get_user_model()


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


class ReviewsViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = ReviewFilter
    pagination_class = PageNumberPagination

    # permission_classes = (IsAdminOrReadOnly,)

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
            author=User.objects.get(username='bingobongo'),
            title=self.get_title(),
        )
