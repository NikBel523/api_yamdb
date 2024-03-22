# Generated by Django 3.2 on 2024-03-22 15:18

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yam_auth', '0004_remove_yamuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamuser',
            name='username',
            field=models.CharField(error_messages={'max_length': 'Имя пользователя не более 150 символов.', 'unique': 'Пользователь с таким именем существует'}, help_text='Не больше 150 символов. Буквы, цифры и @/./+/-/_ только.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), django.core.validators.RegexValidator(message='Имя пользователя не может быть "me".', regex='me')], verbose_name='username'),
        ),
    ]
