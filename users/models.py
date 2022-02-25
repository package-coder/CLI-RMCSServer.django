import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from rest_framework.permissions import DjangoModelPermissions

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tnxCode = models.CharField(max_length=3)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class CustomDjangoModelPermission(DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map) # you need deepcopy when you inherit a dictionary type 
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']