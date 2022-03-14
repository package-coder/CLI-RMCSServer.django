
from dataclasses import fields
from .models import (
    AFPrefix,
    AFPurchaseTransactionItem,
    AFTransactionHistory,
    AFTransactionItem,
    AFTransactionStatus,
    AFTransactionType,
    AFType,
    AFRequestItem,
    AFRequestHistory,
    AFPersonTransactionRecord
)
from rest_framework import serializers


class BaseRepresentAFMixin:
    
    def to_represent_af(self, instance):
        
        instance['prefix'] = AFPrefix.objects.get(pk=instance['prefix']).name
        instance['status'] = AFTransactionStatus.objects.get(pk=instance['status']).name

        return instance


class BaseHistorySerializer(serializers.ModelSerializer):
    """
        A base history serializer is the base class or template for retrieving and creating 
        a bulk data (parent-child models - one to one relationship) specifically the 
        AFRequestHistory + AFRequestItems..

        This Base Serializer can be use in RequestHistory and TransactionHistory
    """
    
    history_class = None
    history_item_class = None

    def get_history(self, validated_data):
        history_model = self.get_history_class()
        history = history_model.objects.create(**validated_data)
        return history

    """
        Get history items needs to override as for request items and transaction items
        might be in different structure
    """
    def get_history_items(self, validated_data):
        raise NotImplementedError

    def create_history_item(self, history, data):
        item_model = self.get_item_class()
        item = item_model.objects.create(**data)
        return item

    def get_history_class(self):
        return self.history_class

    def get_item_class(self):
        return self.history_item_class

    """
        To represent item needs to override as for creation of the history item 
        with different structure of data
    """
    def to_represent_item(self, history, item):
        raise NotImplementedError

    def create(self, validated_data):
        items = self.get_history_items(validated_data)
        history = self.get_history(validated_data)

        for i in items:
            data = self.to_represent_item(history, i)
            self.create_history_item(history, data)

        return history


class PurchaseTransactionMixin(object):

    purchase_item_class = None

    def get_purchase_entry(self, data):
        raise NotImplementedError

    def get_transaction_type(self, history):
        raise NotImplementedError

    def to_represent_puchase_item(self, entry, item):
        raise NotImplementedError

    def create_purchase_item(self, data):
        purchase_item = self.purchase_item_class.objects.create(**data)

        return purchase_item

    def add_purchase_item(self, history, item, entry):
        transaction_type = self.get_transaction_type(history)

        if transaction_type != 'TYPE_PURCHASE':
            return

        data = self.to_represent_puchase_item(entry, item)
        self.create_purchase_item(data)

    def create_history_item(self, history, data):
        entry = self.get_purchase_entry(data)
        item = super().create_history_item(history, data)

        self.add_purchase_item(history, item, entry)

        return item


class AFPersonTransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFPersonTransactionRecord
        fields = '__all__'


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



class AFRequestItemSerializer(serializers.ModelSerializer):   
    class Meta:
        model = AFRequestItem
        fields = '__all__'


class AFRequestItemReadOnlySerializer(AFRequestItemSerializer):
    af_type = AFTypeSerializer()


class AFRequestSerializer(BaseRepresentAFMixin, BaseHistorySerializer):
    request_items = AFRequestItemSerializer(write_only=True, many=True)
    control_number = serializers.IntegerField(read_only=True)

    history_class = AFRequestHistory
    history_item_class = AFRequestItem

    class Meta:
        model = AFRequestHistory
        fields = '__all__'

    
    def get_history_items(self, validated_data):
        return validated_data.pop('request_items')
    
    def to_represent_item(self, history, item):
        data = {
            'request_history': history,
            **item
        }

        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = super().to_represent_af(data)
        
        data['request_type'] = AFTransactionType.objects.get(pk=data['request_type']).name
        
        items_serializer = AFRequestItemReadOnlySerializer(
            AFRequestItem.objects.filter(request_history=data['id']), 
            many=True
        )

        data['request_items'] = items_serializer.data
        return data
    

class AFPurchaseRequestSerializer(PurchaseTransactionMixin, AFRequestSerializer):
    request_items = AFRequestItemSerializer(write_only=True, many=True)
    purchase_item_class = None

    def get_purchase_entry(self, data):
        return data.pop('entry')

    def get_transaction_type(self, history):
        return history.request_type.id
    
    def to_represent_puchase_item(self, entry, item):
        data = {
            'request_item': item,
            **entry
        }

        return data




class AFPurchaseTransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFPurchaseTransactionItem
        fields = '__all__'


class AFTransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFTransactionItem
        fields = '__all__'
   

class AFTransactionItemWriteOnlySerializer(AFTransactionItemSerializer):
    entry = AFPurchaseTransactionItemSerializer()


class AFTransactionSerializer(BaseRepresentAFMixin, BaseHistorySerializer):
    transaction_items = AFTransactionItemSerializer(write_only=True, many=True)

    control_number = serializers.IntegerField(read_only=True)
    issued_to = AFPersonTransactionRecordSerializer()

    history_class = AFTransactionHistory
    history_item_class = AFTransactionItem

    class Meta:
        model = AFTransactionHistory
        fields = '__all__'

    def get_person_record(self, data):
        person_record = AFPersonTransactionRecord.objects.create(**data)

        return person_record

    def get_history_items(self, validated_data):
        transaction_items = validated_data.pop('transaction_items')
        return transaction_items

    def to_represent_item(self, history, item):
        data = {
            'transaction_history': history,
            **item
        }

        return data

    def get_history(self, validated_data):
        validated_data['issued_to'] = self.get_person_record(validated_data['issued_to'])
        history = super().get_history(validated_data)
        return history

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = super().to_represent_af(data)


        transaction_items = AFTransactionItem.objects.filter(transaction_history=data['id'])
        items_serializer = AFTransactionItemSerializer(transaction_items, many=True)

        data['transaction_type'] = AFTransactionType.objects.get(pk=data['transaction_type']).name
        data['transaction_items'] = items_serializer.data

        return data


class AFRequestTransactionSerializer(PurchaseTransactionMixin, AFTransactionSerializer):
    purchase_item_class = None

    
    def get_purchase_entry(self, data):
        return None
    
    def get_transaction_type(self, history):
        return history.transaction_type.id
    
    def to_represent_puchase_item(self, entry, item):
        data = {
            'transaction_item': item,
            **entry
        }

        return data


    def get_history_items(self, validated_data):
        request_history = validated_data['request_history']
        request_items = AFRequestItem.objects.filter(request_history=request_history)

        return request_items

    def get_history(self, validated_data):
        history = super().get_history(validated_data)
        history.transaction_type = validated_data['request_history'].request_type
        history.save()

        return history
    
    def to_represent_item(self, history, item):
        data = {
            'transaction_history': history,
            'request_item': item,
            'af_type': item.af_type,
            'quantity': item.quantity
        }

        return data


class AFPurchaseTransactionSerializer(PurchaseTransactionMixin, AFTransactionSerializer):
    transaction_items = AFTransactionItemWriteOnlySerializer(write_only=True, many=True)
    purchase_item_class = AFPurchaseTransactionItem

    def get_purchase_entry(self, data):
        return data.pop('entry')

    def get_transaction_type(self, history):
        return history.transaction_type.id
    
    def to_represent_puchase_item(self, entry, item):
        data = {
            'transaction_item': item,
            **entry
        }

        return data

class AFTransactionItemReadOnlySerializer(AFTransactionItemSerializer):
    af_type = AFTypeSerializer()
    request_item = AFRequestItemSerializer()
    transaction_history = AFTransactionSerializer()
 