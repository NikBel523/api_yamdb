from django.contrib.auth import get_user_model
from rest_framework import serializers

# from api_yamdb.custom_auth.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'username',)


class ConfirmationCodeSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ('confirmation_code',)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio']
