from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Модель пользователя."""
    role = models.CharField(max_length=20, choices=(('user', 'user'),
                                                    ('admin', 'admin'),
                                                    ('moderator', 'moderator'))
                            )
    bio = models.TextField(blank=True)
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(_('email address'), blank=True, unique=True)
