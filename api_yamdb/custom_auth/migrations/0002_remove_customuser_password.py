# Generated by Django 3.2 on 2024-03-20 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password',
        ),
    ]