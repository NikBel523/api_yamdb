from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from reviews.models import Category, Genre, Title

from api.filters import TitleFilter
from api.mixins import (
    AdminManagebleMixin,
    AllowedMethodsMixin,
    PatchRolesPermissionMixin,
    SearchMixin,
)
from api.permissions import ManagesOnlyAdmin
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


User = get_user_model()


class CategoryViewSet(SearchMixin, AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SearchMixin, AdminManagebleMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(AllowedMethodsMixin, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (ManagesOnlyAdmin,)


class ReviewsViewSet(PatchRolesPermissionMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        # Добавляю .all() что бы певратить объект RelatedManager в QuerySet
        # Это обеспечивает работу пагинатора, который не может в RelatedManager
        # RelatedManager не работает для слайсов и индексации
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=User.objects.get(username=self.request.user),
            title=self.get_title(),
        )


class CommentViewSet(PatchRolesPermissionMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_specific_review(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.get(pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_specific_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=User.objects.get(username=self.request.user),
            review=self.get_specific_review(),
        )
