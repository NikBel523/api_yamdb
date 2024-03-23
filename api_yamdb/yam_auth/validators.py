# from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

"""
class NotMeValidator(RegexValidator):
    regex = r'^(?!me$).+'
    message = 'me недопустимо в качестве имени пользователя.'
    flags = 0
"""


def not_me_validator(value):
    if value and value.casefold() == 'me':
        raise ValidationError('me недопустимо в качестве имени пользователя.')
    return value
