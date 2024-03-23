from django.contrib.auth import get_user_model
from rest_framework import exceptions, filters, viewsets

from api.permissions import IsAdmin
from api.serializers import UserProfileSerializer

User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

    def _is_me(self):
        return self.kwargs.get('username', None) == 'me'

    def get_object(self):
        if self._is_me():
            return User.objects.get(pk=self.request.user.pk)
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self._is_me():
            raise exceptions.MethodNotAllowed(method='delete')
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self._is_me():
            serializer.validated_data.pop('role', None)
        serializer.save()
