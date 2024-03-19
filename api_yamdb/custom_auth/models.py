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
    # думаю, можно наследовать базовое поле, так как валидатор и всё нужное
    # username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField('email address', blank=False, unique=True)

    def __str__(self):
        return self.username

    class Meta:
        swappable = "AUTH_USER_MODEL"
