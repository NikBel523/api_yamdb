from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Title

from api.filters import TitleFilter
from api.permissions import ManagesOnlyAdmin
from api.serializers.title import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'retrive', 'delete')
    permission_classes = (ManagesOnlyAdmin,)
