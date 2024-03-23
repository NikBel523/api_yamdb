import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from yam_auth.validators import NotMeValidator

User = get_user_model()


def _generate_confirmation_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(5))


def _send_confirmation_email(email, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = settings.EMAIL_HOST_USER

    message = EmailMessage(subject, message, from_email, [email])
    message.send()


class UserSerializer(serializers.Serializer):
    not_me_validator = NotMeValidator()

    username = serializers.SlugField(
        validators=[
            AbstractUser.username_validator,
            not_me_validator],
        max_length=150)
    email = serializers.EmailField(max_length=254)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user = None

        users = User.objects.filter(username=username)
        if len(users) == 0:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                raise serializers.ValidationError(
                    {'email': f'EMail {email} уже используется '
                     ' другим пользователем'})
            user = User.objects.create(**validated_data)
        else:
            user = users.first()
            if user.email != email:
                raise serializers.ValidationError(
                    {'email': 'EMail не совпадает с адресом пользователя'})

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
