from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    prima_id = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, null=True)
