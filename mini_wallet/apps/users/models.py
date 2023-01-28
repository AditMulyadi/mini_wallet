from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    xid = models.TextField()
    is_active = models.BooleanField(default=True)