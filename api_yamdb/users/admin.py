from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': (
            'role', 'is_active', 'is_staff', 'is_superuser'
        )}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Bio'), {'fields': ('bio', )}),
    )
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'role',
        'bio',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name'
    )
    ordering = ('email',)
    list_editable = ('role',)
