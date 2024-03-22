from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class YamUserAdmin(UserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role')
    list_filter = ()
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(get_user_model(), YamUserAdmin)
