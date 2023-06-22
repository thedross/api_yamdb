from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

import users.constants as const
from users.validators import validate_username


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Ник',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex='^[\\w-]+$',
                message='Ник содержит недопустимые символы.'
            ),
            validate_username
        ]
    )
    email = models.EmailField(
        verbose_name='e-mail',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=150,
        choices=const.CHOICES_ROLE,
        default=const.USER,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        max_length=254,
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == const.USER

    @property
    def is_moderator(self):
        return self.role == const.MODERATOR

    @property
    def is_admin(self):
        return self.role == const.ADMIN

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
