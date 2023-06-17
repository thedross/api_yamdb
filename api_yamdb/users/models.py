from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_moderator = models.BooleanField('Модератор', default=False)
    is_admin = models.BooleanField(
        'Администратор',
        default=False,
        help_text='True if user is admin'
    )
    bio = models.TextField('Биография', blank=True)

    def __str__(self):
        return self.username
