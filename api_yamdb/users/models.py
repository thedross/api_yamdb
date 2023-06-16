from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    moderator = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username