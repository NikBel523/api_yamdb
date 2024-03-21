from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Title

from api.permissions import IsReviewPatcherOrReadOnly
from api.serializers.review import CommentSerializer, ReviewSerializer


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
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsReviewPatcherOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')

    def get_specific_review(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.get(pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_specific_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_specific_review(),
        )
