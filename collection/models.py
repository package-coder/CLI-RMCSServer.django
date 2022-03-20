import uuid

from django.db import models
from accounts.models import (
    Person, User
)

from accountable_forms.models import (
    AFItem
)
# Create your models here.


class PersonAccount(Person):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)


# Possible values - GENERAL PROPER, PROPER
class Fund(models.Model):
    code = models.CharField(max_length=20, primary_key=True, editable=False)
    title = models.CharField(max_length=50)


# Possible values - REVENUE, ...
class ItemType(models.Model):
    id = models.CharField(max_length=30, primary_key=True, editable=False)
    name = models.CharField(max_length=20)


# Possible values - DRAFT, ACTIVE, INACTIVE
class ItemState(models.Model):
    id = models.CharField(max_length=30, primary_key=True, editable=False)
    name = models.CharField(max_length=20)


# Possible values - POSTED, CANCELLED
class ReceiptState(models.Model):
    id = models.CharField(max_length=30, primary_key=True, editable=False)
    name = models.CharField(max_length=20)


class TransactionType(models.Model):
    pass


class ItemAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    state = models.ForeignKey(ItemState, on_delete=models.RESTRICT)
    type = models.ForeignKey(ItemType, on_delete=models.RESTRICT)
    title = models.CharField(max_length=200)
    fund = models.ForeignKey(Fund, on_delete=models.RESTRICT, null=True)


class CashRecept(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer_account = models.ForeignKey(
        PersonAccount, on_delete=models.RESTRICT, null=True)
    payer_name = models.CharField(max_length=100, null=True, blank=True)
    payer_address = models.CharField(max_length=200, null=True, blank=True)
    operator = models.ForeignKey(User, on_delete=models.RESTRICT)
    af_item = models.ForeignKey(AFItem, on_delete=models.RESTRICT)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.RESTRICT)
    transaction_date = models.DateField()
    state = models.ForeignKey(ReceiptState, on_delete=models.RESTRICT)
    amount = models.DecimalField()
    total_cash = models.DecimalField()
    total_non_cash = models.DecimalField()
    collection_type = None
    remittance = None
    remarks = None


class CashReceiptItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
