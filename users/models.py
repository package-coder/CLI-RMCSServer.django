import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tnxCode = models.CharField(max_length=3)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"