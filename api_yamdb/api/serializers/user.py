import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from yam_auth.constants import MAX_LENGTH_150, MAX_LENGTH_254
from yam_auth.validators import not_me_validator

User = get_user_model()


def _generate_confirmation_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits)
                   for i in range(settings.CONFIRMATION_CODE_LENGTH))


def _send_confirmation_email(email, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = settings.EMAIL_HOST_USER

    message = EmailMessage(subject, message, from_email, [email])
    message.send()


class UserSerializer(serializers.Serializer):

    username = serializers.SlugField(
        validators=[
            AbstractUser.username_validator,
            not_me_validator],
        max_length=MAX_LENGTH_150)
    email = serializers.EmailField(max_length=MAX_LENGTH_254)

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']

        # Нам нужно обработать сценарии создания нового юзера
        # и повторного запроса confirmation_code существующего
        # если новый, то надо убедиться, что name и email не существуют
        # в базе. Если повторный - то что у него указан свой email и
        # name уже сеть в базе.

        user_by_name = User.objects.filter(username=username).first()
        user_by_mail = User.objects.filter(email=email).first()

        if not user_by_name and not user_by_mail:
            return attrs

        if user_by_name != user_by_mail:
            if getattr(
                    user_by_name,
                    'username', None) != getattr(
                    user_by_mail,
                    'username', None):
                raise serializers.ValidationError(
                    {'email': f'EMail {email} уже используется '
                     ' другим пользователем'})

            if getattr(
                    user_by_name,
                    'email', None) != getattr(
                    user_by_mail,
                    'email', None):
                raise serializers.ValidationError(
                    {'email': 'EMail не совпадает с адресом пользователя'})

        return attrs

    def create(self, data):
        defaults = data.copy()
        username = defaults.pop('username', '')
        user, _ = User.objects.get_or_create(
            username=username, defaults=defaults)

        user.confirmation_code = _generate_confirmation_code()
        user.save()
        _send_confirmation_email(user.email, user.confirmation_code)

        return user


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для серииализации confirmation_code."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if user.confirmation_code != attrs['confirmation_code']:
            raise serializers.ValidationError(
                'Неправильный код подтверждения',
            )

        return True
