from custom_auth.models import CustomUser
from django.contrib import admin

# Суперюзер: login: super /EMail: super@fake.com /pwd: yandex22.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role')


admin.site.register(CustomUser, CustomUserAdmin)
