from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models

from yam_auth.constants import (
    LENGTH_CONF_CODE,
    MAX_LENGTH_ROLE,
    ROLE_USER,
    ROLE_ADMIN,
    ROLE_MODERATOR
)


class YamUser(AbstractUser):
    """Модель пользователя."""
    username_validator = UnicodeUsernameValidator()
    username_validator_2 = RegexValidator(
        regex=r'^(?!me$).+',
        message='Имя пользователя не может быть "me".')
    role = models.CharField(max_length=MAX_LENGTH_ROLE,
                            default=ROLE_USER,
                            choices=(
                                (ROLE_USER, 'user'),
                                (ROLE_ADMIN, 'admin'),
                                (ROLE_MODERATOR, 'moderator')
                            ))
    bio = models.TextField(blank=True)
    email = models.EmailField('email address', blank=False, unique=True)
    confirmation_code = models.CharField(
        max_length=LENGTH_CONF_CODE, blank=True, null=True)
    #  Поле password является обязательным и определяется в классе
    #  AbstractBaseUser. По ТЗ данное поле никак не используется,
    #  потому его необходимо переопределть как None.
    password = None
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('Не больше 150 символов. Буквы, цифры и @/./+/-/_ только.'),
        validators=[username_validator, username_validator_2],
        error_messages={
            'unique': ("Пользователь с таким именем существует"),
            'max_length': "Имя пользователя не более 150 символов.",
        },
    )

    @property
    def is_admin(self):
        if self.role == ROLE_ADMIN and self.is_superuser and self.is_staff:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == ROLE_MODERATOR:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.is_superuser is True:
            self.role = ROLE_ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
