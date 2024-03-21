from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers.user import ConfirmationCodeSerializer, UserSerializer
from custom_auth.models import CustomUser


def _generate_token(user):
    token = AccessToken.for_user(user)
    return token


class UserViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ConfirmationCodeSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.initial_data.get('confirmation_code')
        user = get_object_or_404(
            CustomUser, confirmation_code=confirmation_code)
        if user is None:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST)
        token = _generate_token(user)
        headers = self.get_success_headers(serializer.data)
        print(headers)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK, headers=headers)
