import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tnxCode = models.CharField(max_length=3, blank=True)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birthDate = models.DateField()
