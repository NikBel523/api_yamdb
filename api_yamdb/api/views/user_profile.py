from django.contrib.auth import get_user_model
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAdmin
from api.serializers import UserProfileSerializer

User = get_user_model()


"""
class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'post', 'patch', 'delete'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'POST' or request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            self.perform_destroy(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
"""

# TODO: надо перейти на @action


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
