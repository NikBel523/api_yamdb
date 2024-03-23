from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from yam_auth.constants import (
    MAX_LENGTH_150,
    ROLE_ADMIN,
    ROLE_MODERATOR,
    ROLE_USER,
)
from yam_auth.validators import not_me_validator


class YamUser(AbstractUser):
    """Модель пользователя."""

    role = models.CharField(max_length=MAX_LENGTH_150,
                            default=ROLE_USER,
                            choices=(
                                (ROLE_USER, 'user'),
                                (ROLE_ADMIN, 'admin'),
                                (ROLE_MODERATOR, 'moderator')
                            ))
    bio = models.TextField(blank=True)
    email = models.EmailField('email address', blank=False, unique=True)
    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH, blank=True, null=True)

    username = models.CharField(
        'username',
        max_length=MAX_LENGTH_150,
        unique=True,
        help_text='Не больше 150 символов. Буквы, цифры и @/./+/-/_ только.',
        validators=[AbstractUser.username_validator, not_me_validator],
        error_messages={
            'unique': "Пользователь с таким именем существует",
            'max_length': "Имя пользователя не более 150 символов.",
        },
    )

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN or (self.is_superuser and self.is_staff)

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = ROLE_ADMIN

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
