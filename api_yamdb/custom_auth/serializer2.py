from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email']
        
    def validate(self, data):
        username = data.get('username')
        if not re.search(r'^[\w.@+-]+$', username):
            raise ValidationError('Имя пользователя не соответствует спецификации')
        return data