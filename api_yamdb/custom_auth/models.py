from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    role = models.CharField(max_length=20, choices=(('user', 'user'),
                                                    ('admin', 'admin'),
                                                    ('moderator', 'moderator'))
                            )
    bio = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField('email address', blank=False, unique=True)

    def __str__(self):
        return self.username
