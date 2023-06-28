from django.contrib.auth.models import AbstractUser
from django.db import models

import users.constants as const
from users.validators import validate_username


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Ник',
        max_length=const.MAX_NAME_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username]
    )
    email = models.EmailField(
        verbose_name='e-mail',
        max_length=const.MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=const.MAX_NAME_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=const.MAX_NAME_LENGTH,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role) for role, verbose_name in const.CHOICES_ROLE),
        choices=const.CHOICES_ROLE,
        default=const.USER,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == const.MODERATOR

    @property
    def is_admin(self):
        return (self.role == const.ADMIN) or self.is_staff or self.is_superuser

    class Meta:
        ordering = ('email', 'username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
