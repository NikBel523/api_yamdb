
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

_User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = _User
        fields = '__all__'


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для серииализации confirmation_code."""
