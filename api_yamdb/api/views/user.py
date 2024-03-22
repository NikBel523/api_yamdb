import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from api.serializers import ConfirmationCodeSerializer, UserSerializer

_User = get_user_model()


def _generate_confirmation_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(5))


def _send_confirmation_email(email, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'no-reply@example.com'

    message = EmailMessage(subject, message, from_email, [email])
    message.send()


def _generate_token(user):
    token = AccessToken.for_user(user)
    return token


class SingUpViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):
    queryset = _User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        self._validate_request()
        user = _User.objects.filter(
            username=request.data['username'])

        return self._process_existing_user(
            user.first()) if user else self._process_new_user()

    # проверяем, что пришло имя и мыло, и имя не равно me
    def _validate_request(self):
        name = self.request.data.get('username')
        email = self.request.data.get('email')
        result = {}
        # очень бредовый тест, поэтому, приходится делать так
        if not name:
            result['username'] = ['Нет имени']
        if not email:
            result['email'] = ['Нет мыла']

        if result:
            raise serializers.ValidationError(result)

        if name.casefold() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя пользователя me', 'username')

    def _process_existing_user(self, user):
        email = self.request.data['email']
        if user.email != email:
            return Response("Неправильный EMail",
                            status.HTTP_400_BAD_REQUEST)
        user.confirmation_code = _generate_confirmation_code()
        user.save()
        _send_confirmation_email(user.email, user.confirmation_code)

        return Response(
            {'username': user.username, 'email': user.email},
            status=status.HTTP_200_OK)

    def _process_new_user(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.confirmation_code = _generate_confirmation_code()
        user.save()
        _send_confirmation_email(user.email, user.confirmation_code)

        return Response({
            'username': serializer.data['username'],
            'email': serializer.data['email']
        }, status=status.HTTP_200_OK)


class ObtainTokenView(TokenViewBase):

    serializer_class = ConfirmationCodeSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        confirmation_code = serializer.initial_data.get('confirmation_code')

        if not request.data or not request.data.get('username'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = None
        try:
            username = request.data['username']
            user = _User.objects.get(username=username)
        except _User.DoesNotExist:
            return Response(
                {'error': 'Пользователь с таким именем не существует'},
                status=status.HTTP_404_NOT_FOUND)

        if user.confirmation_code != confirmation_code:
            return Response('Неправильный код подтверждения',
                            status=status.HTTP_400_BAD_REQUEST)

        token = _generate_token(user)

        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)
