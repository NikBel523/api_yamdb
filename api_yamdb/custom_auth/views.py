import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
# from django.core.mail.backends.filebased import EmailBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from custom_auth.serializers import (
    ConfirmationCodeSerializer,
    UserSerializer
)

User = get_user_model()


def generate_confirmation_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(5))


def send_confirmation_email(email, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'no-reply@example.com'
    to_email = email
    email = EmailMessage(subject, message, from_email, [to_email])
    email.content_subtype = 'html'
    email.send()


def generate_token(user):
    token = AccessToken.for_user(user)
    return token


class UserViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    queryset = User.objects.all()
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


class MyTokenObtainPairView(TokenViewBase):
    pass


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ConfirmationCodeSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.initial_data.get('confirmation_code')
        user = get_object_or_404(User, confirmation_code=confirmation_code)
        username = user.get_username()
        print(username)
        if user is None:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            username = request.data['username']
            print(username)
            User.objects.get(username=username)
            print(User.objects.get(username=username))
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь с таким именем не существует'},
                status=status.HTTP_404_NOT_FOUND)
        token = generate_token(user)
        headers = self.get_success_headers(serializer.data)
        print(headers)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK, headers=headers)


obtain_auth_token = AuthViewSet
