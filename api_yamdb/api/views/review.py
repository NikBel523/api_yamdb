from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsReviewPatcherOrReadOnly
from api.serializers.review import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class _BaseCommentingViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')
    permission_classes = (IsAuthenticatedOrReadOnly, IsReviewPatcherOrReadOnly)


class ReviewsViewSet(_BaseCommentingViewSet):
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
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(_BaseCommentingViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )
