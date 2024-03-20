import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_email(user.email, confirmation_code)
        return user


class ConfirmationCodeSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ('confirmation_code',)



