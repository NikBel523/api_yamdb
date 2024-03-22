
from django.core.exceptions import ValidationError
from rest_framework import serializers

from custom_auth.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate_last_name(self, value):
        if len(value) > 150:
            raise ValidationError(
                detail='Слишком длинная фамилия.',
                code='last_name_too_long')
        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise ValidationError(
                detail='Слишком длинное имя.',
                code='first_name_too_long')
        return value


class ConfirmationCodeSerializer(serializers.Serializer):

    class Meta:
        model = CustomUser
        fields = ('confirmation_code',)
