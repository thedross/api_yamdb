from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(
        default=False,
        help_text='True if user is admin'
    )

    def __str__(self):
        return self.username
