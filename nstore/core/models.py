from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)  # add email field
    username = models.CharField(max_length=20, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']