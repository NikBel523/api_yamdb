from django.contrib.auth.models import AbstractUser
from django.db import models

# Суперюзер: login: super /EMail: super@fake.com /pwd: yandex22.


class CustomUser(AbstractUser):
    """Модель пользователя."""
    role = models.CharField(max_length=20,
                            default='user',
                            choices=(('user', 'user'),
                                     ('admin', 'admin'),
                                     ('moderator', 'moderator'))
                            )
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField('email address', blank=False, unique=True)
    confirmation_code = models.CharField(
        max_length=5, unique=True, blank=True, null=True)
    password = models.CharField('password', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        swappable = "AUTH_USER_MODEL"
