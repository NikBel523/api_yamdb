from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from custom_auth.serializer2 import UserProfileSerializer


class UserProfileViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        if user != serializer.instance:
            return Response(
                {'error': 'Вы не можете изменять профиль другого пользователя'},
                status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
