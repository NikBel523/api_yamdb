from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly
from api.serializers.title import TitleSerializer
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')
    permission_classes = (AdminOrReadOnly,)
