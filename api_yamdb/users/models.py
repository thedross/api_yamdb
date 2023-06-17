from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.username
