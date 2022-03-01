import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=100)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=True)
    tnxCode = models.CharField(max_length=3, blank=True)

    objects = UserManager()


    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

