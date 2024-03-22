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

    password = None
    groups = None
    user_permissions = None

    def save(self, *args, **kwargs):
        if self.is_superuser is True:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        swappable = "AUTH_USER_MODEL"
        ordering = ('username', )
