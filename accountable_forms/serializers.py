from dataclasses import field

from users.models import User
from .models import (
    AFType,
    AFRequestItem,
    AFRequestHistory
)
from rest_framework import serializers


class AFTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFType
        fields = '__all__'

class AFRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFRequestItem
        fields = '__all__'

class AFRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AFRequestHistory
        fields = '__all__'