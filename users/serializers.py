
import uuid
from rest_framework import serializers
from .models import (
    User,
    Role
)

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, default=uuid.uuid4)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        
        user = User.objects.create(username=username, **validated_data)
        user.set_password(password)

        return user

    def update(self, instance, validated_data):
        print(validated_data, instance)
        password = validated_data.get('password', None)
        
        if password is not None:
            validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

    def perform_create(self, serializer):
        return serializer.save()

class RoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Role
        fields = '__all__'