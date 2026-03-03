from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    approved = models.BooleanField(default=True)