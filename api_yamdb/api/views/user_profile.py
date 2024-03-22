from django.contrib.auth import get_user_model
from rest_framework import exceptions, filters, viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import IsAdmin
from api.serializers.user_profile import UserProfileSerializer

_User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = _User.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def _is_me(self):
        return self.kwargs.get('username', None) == 'me'

    def get_object(self):
        if self._is_me():
            return _User.objects.get(pk=self.request.user.pk)
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self._is_me():
            raise exceptions.MethodNotAllowed(method='delete')
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self._is_me():
            serializer.validated_data.pop('role', None)
        serializer.save()
