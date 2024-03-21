import re

from django.forms import ValidationError
from rest_framework import serializers

from custom_auth.models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'last_name',
            'first_name',
            'username',
            'email',
            'bio',
            'role']

        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, value):
        if not re.search(r'^[\w.@+-]+\Z', value):
            raise ValidationError(
                'Имя пользователя не соответствует спецификации')

        if len(value) > 150:
            raise ValidationError(
                "Имя пользователя не должно быть длиннее 150 символов")

        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise ValidationError(
                "Имя пользователя first_name не должно быть длиннее 150 символов")

        return value
