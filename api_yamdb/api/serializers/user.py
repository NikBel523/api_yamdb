
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

_User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = _User
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
        model = _User
        fields = ('confirmation_code',)
