from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_moderator',
        'is_admin'
    )
    list_filter = (
        'is_staff',
        'is_moderator',
        'is_admin'
    )
    search_fields = (
        'email',
        'first_name',
        'last_name'
    )
    ordering = ('email',)
