from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
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
