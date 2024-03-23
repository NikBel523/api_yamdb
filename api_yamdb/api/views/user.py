from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from api.serializers import ConfirmationCodeSerializer, UserSerializer

User = get_user_model()


def _generate_token(user):
    token = AccessToken.for_user(user)
    return token


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ObtainTokenView(TokenViewBase):

    serializer_class = ConfirmationCodeSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = _generate_token(
            User.objects.get(
                username=request.data['username']))

        return Response({'token': str(token)}, status=status.HTTP_200_OK)
