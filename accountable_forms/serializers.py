from dataclasses import fields

from django.shortcuts import get_object_or_404
from .models import (
    AFItem,
    AFPrefix,
    AFPurchaseTransactionItem,
    AFTransactionHistory,
    AFTransactionItem,
    AFTransactionStatus,
    AFTransactionType,
    AFType,
    AFRequestItem,
    AFRequestHistory,
    PersonTransactionRecord
)
from .mixins import (
    PurchaseTransactionMixin,
    BaseRepresentAFMixin, AFItemPurchaseMixin
)

from rest_framework import serializers


# TODO request item status - if the transaction item rejects it

class BaseHistorySerializer(serializers.ModelSerializer):
    """
        A base history serializer is the base class or template for retrieving and creating 
        a bulk data (parent-child models - one to one relationship) specifically the 
        AFRequestHistory + AFRequestItems

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


class AFPersonTransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonTransactionRecord
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


class AFPurchaseTransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFPurchaseTransactionItem
        fields = '__all__'


class AFRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFRequestItem
        fields = '__all__'


class AFRequestItemReadOnlySerializer(AFRequestItemSerializer):
    af_type = AFTypeSerializer()


class AFRequestItemWriteOnlySerializer(AFRequestItemSerializer):
    entry = AFPurchaseTransactionItemSerializer()


class AFRequestSerializer(BaseRepresentAFMixin, BaseHistorySerializer):
    request_items = AFRequestItemSerializer(write_only=True, many=True)

    history_class = AFRequestHistory
    history_item_class = AFRequestItem

    class Meta:
        model = AFRequestHistory
        fields = '__all__'
        read_only_fields = ['prefix', 'status', 'control_number']

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

        data['request_type'] = AFTransactionType.objects.get(
            pk=data['request_type']).name

        data['request_items'] = AFRequestItemReadOnlySerializer(
            AFRequestItem.objects.filter(request_history=data['id']),
            many=True
        ).data

        for item in data['request_items']:
            item['entry'] = AFPurchaseTransactionItemSerializer(
                AFPurchaseTransactionItem.objects.filter(
                    request_item=item['id']),
                many=True
            ).data

        return data


class AFPurchaseRequestSerializer(PurchaseTransactionMixin, AFRequestSerializer):
    request_items = AFRequestItemWriteOnlySerializer(
        write_only=True, many=True)
    purchase_item_class = AFPurchaseTransactionItem

    def get_purchase_entry(self, data):
        return data.pop('entry')

    def get_transaction_type(self, history):
        return history.request_type.id

    def to_represent_purchase_item(self, entry, item):
        data = {
            'request_item': item,
            **entry
        }

        return data

    def add_af_item(self, history, purchase_item, transaction_item):
        pass


class AFTransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFTransactionItem
        fields = '__all__'


class AFTransactionEntryItemSerializer(AFTransactionItemSerializer):
    entry = AFPurchaseTransactionItemSerializer()


class AFTransactionSerializer(BaseRepresentAFMixin, BaseHistorySerializer):
    transaction_items = AFTransactionItemSerializer(write_only=True, many=True)

    issued_to = AFPersonTransactionRecordSerializer()

    history_class = AFTransactionHistory
    history_item_class = AFTransactionItem

    class Meta:
        model = AFTransactionHistory
        fields = '__all__'
        read_only_fields = ['prefix', 'status',
                            'control_number', 'issued_date']

    def get_person_record(self, data):
        person_record = PersonTransactionRecord.objects.create(**data)

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
        validated_data['issued_to'] = self.get_person_record(
            validated_data['issued_to'])
        history = super().get_history(validated_data)
        return history

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = super().to_represent_af(data)

        data['transaction_type'] = AFTransactionType.objects.get(
            pk=data['transaction_type']).name
        data['transaction_items'] = AFTransactionItemSerializer(
            AFTransactionItem.objects.filter(transaction_history=data['id']),
            many=True
        ).data

        for item in data['transaction_items']:
            item['entry'] = AFPurchaseTransactionItemSerializer(
                AFPurchaseTransactionItem.objects.filter(
                    transaction_item=item['id']),
                many=True
            ).data

        return data


class AFRequestTransactionSerializer(AFItemPurchaseMixin,
                                     PurchaseTransactionMixin,
                                     AFTransactionSerializer):
    transaction_items = serializers.ListSerializer(
        child=serializers.UUIDField(), write_only=True)
    purchase_item_class = AFPurchaseTransactionItem

    def get_purchase_entry(self, data):
        request_item = data['request_item']
        entry = get_object_or_404(
            self.purchase_item_class, request_item=request_item)
        return entry

    def get_transaction_type(self, history):
        return history.request_history.request_type.id

    def to_represent_purchase_item(self, entry, item):
        entry.transaction_item = item

        return entry

    def create_purchase_item(self, data):
        data.save()

        return data

    @staticmethod
    def validate_request_item(request_item, to_approve_items):
        is_approve = request_item.id in to_approve_items

        status = 'STATUS_COMPLETED' if is_approve else 'STATUS_CANCELLED'
        request_item.status = AFTransactionStatus.objects.get(pk=status)
        request_item.save()

        return is_approve

    def get_history_items(self, validated_data):

        to_approve_items = validated_data.pop('transaction_items')
        request_history = validated_data['request_history']
        request_items = AFRequestItem.objects.filter(
            request_history=request_history)

        # If list is empty
        if not to_approve_items:
            return request_items

        # Filter all the request_items using uuid passed in transaction_items
        approved_items = list(filter(lambda item: self.validate_request_item(
            item, to_approve_items), request_items))
        return approved_items

    def create(self, validated_data):
        request_history = validated_data['request_history']

        # Check if the current request history is already in the transaction list
        try:
            current_history = self.history_class.objects.get(
                request_history=request_history)
            return current_history
        except AFTransactionHistory.DoesNotExist:
            pass

        history = super().create(validated_data)

        status = AFTransactionStatus.objects.get(pk='STATUS_COMPLETED')
        request_history.status = status
        history.status = status

        request_history.save()
        history.save()
        return history

    def get_history(self, validated_data):
        request_history = validated_data['request_history']
        history = super().get_history(validated_data)
        history.transaction_type = request_history.request_type
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


class AFPurchaseTransactionSerializer(AFItemPurchaseMixin,
                                      PurchaseTransactionMixin,
                                      AFTransactionSerializer):
    transaction_items = AFTransactionEntryItemSerializer(
        write_only=True, many=True)
    purchase_item_class = AFPurchaseTransactionItem

    def get_purchase_entry(self, data):
        return data.pop('entry')

    def get_transaction_type(self, history):
        return history.transaction_type.id

    def to_represent_purchase_item(self, entry, item):
        data = {
            'transaction_item': item,
            **entry
        }

        return data


class AFTransactionItemReadOnlySerializer(AFTransactionItemSerializer):
    af_type = AFTypeSerializer()
    request_item = AFRequestItemSerializer()
    transaction_history = AFTransactionSerializer()


class AFItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFItem
        fields = '__all__'
