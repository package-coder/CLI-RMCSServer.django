
import uuid

from django.contrib.auth.models import (
    Group, 
    Permission
)
from rest_framework import serializers

from .models import (
    User
)

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, default=uuid.uuid4)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        return super().update(instance, validated_data)

    def perform_create(self, serializer):
        return serializer.save()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        group.save()

        return group

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
