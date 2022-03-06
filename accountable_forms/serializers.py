from dataclasses import field

from .models import (
    AFType,
    AFRequestItem,
    AFRequest
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
        model = AFRequest
        fields = '__all__'