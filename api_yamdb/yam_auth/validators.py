from django.core.validators import RegexValidator


class NotMeValidator(RegexValidator):
    regex = r'^(?!me$).+'
    message = 'me недопустимо в качестве имени пользователя.'
    flags = 0
