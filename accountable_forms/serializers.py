
from .models import (
    AFTransactionHistory,
    AFTransactionItem,
    AFTransactionStatus,
    AFTransactionType,
    AFType,
    AFRequestItem,
    AFRequestHistory
)
from rest_framework import serializers


class AFTransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFTransactionStatus
        fields = '__all__'


class AFTransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFTransactionType
        fields = '__all__'


class AFTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFType
        fields = '__all__'


class AFRequestHistorySerializer(serializers.ModelSerializer):
    control_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = AFRequestHistory
        fields = '__all__'


class AFRequestItemSerializer(serializers.ModelSerializer):   
    class Meta:
        model = AFRequestItem
        fields = '__all__'


class AFRequestHistoryWriteOnlySerializer(AFRequestHistorySerializer):
    request_items = AFRequestItemSerializer(write_only=True, many=True)

    def create(self, validated_data):
        request_items = validated_data.pop('request_items')
        request_history = AFRequestHistory.objects.create(**validated_data)
        request_history.save()
       
        for item in request_items:
            AFRequestItem.objects.create(request_history=request_history, **item).save()

        return request_history


class AFRequestItemReadOnlySerializer(AFRequestItemSerializer):
    af_type = AFTypeSerializer()


class AFTransactionHistorySerializer(serializers.ModelSerializer):
    control_number = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = AFTransactionHistory
        fields = '__all__'


class AFTransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFTransactionItem
        fields = '__all__'


class AFTransactionHistoryWriteOnlySerializer(AFTransactionHistorySerializer):
    transaction_items = AFTransactionItemSerializer(write_only=True, many=True)

    def create(self, validated_data):
        transaction_items = validated_data.pop('transaction_items')
        transaction_history = AFTransactionHistory.objects.create(**validated_data)
        transaction_history.save()
       
        for item in transaction_items:
            AFTransactionItem.objects.create(transaction_history=transaction_history, **item).save()

        return transaction_history


class AFTransactionItemReadOnlySerializer(AFTransactionItemSerializer):
    af_type = AFTypeSerializer()
    request_history = AFRequestHistorySerializer()
    transaction_history = AFTransactionHistorySerializer()