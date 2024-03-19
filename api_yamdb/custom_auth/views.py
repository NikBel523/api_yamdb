from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.core.mail.backends.filebased import EmailBackend
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt import tokens
from custom_auth.serializers import ConfirmationCodeSerializer, UserSerializer, UserProfileSerializer
import string
import random

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


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_email(user.email, confirmation_code)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ConfirmationCodeSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        user = User.objects.filter(confirmation_code=confirmation_code)
        if user is None:
            return Response({'error': 'Неверный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)
        token = self.generate_token(user)  # здесь должна быть функция генерации токена
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token}, status=status.HTTP_200_OK, headers=headers)

    def generate_token(user):
        return tokens.AccessToken.for_user(user).access_token


class UserProfileViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    #queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        if user != serializer.instance:
            return Response({'error': 'Вы не можете изменять профиль другого пользователя'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# class UserViewSet(mixins.CreateModelMixin,
#                   mixins.ListModelMixin,
#                   viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (permissions.AllowAny,)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     email = serializer.validated_data['email']
    #     username = 'me' if email == 'me' else email
    #     user = User.objects.create_user(username=username, email=email)
    #     user.save()
    #     return Response({'confirmation_code': 'your_confirmation_code'})

    # def get_confirmation_code(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     email = serializer.validated_data['email']
    #     user = User.objects.filter(email=email).first()
    #     if user:
    #         return Response({'confirmation_code': 'your_confirmation_code'})
    #     else:
    #         return Response({'error': 'User with this email does not exist.'})
