from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly
from api.serializers import TitleReadSerializer, TitleWriteSerializer
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleWriteSerializer
        return TitleReadSerializer
