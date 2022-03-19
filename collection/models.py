import uuid

from django.db import models


# Create your models here.

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


class ItemAccounts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    state = models.ForeignKey(ItemState, on_delete=models.RESTRICT)
    type = models.ForeignKey(ItemType, on_delete=models.RESTRICT)
    title = models.CharField(max_length=200)
    fund = models.ForeignKey(Fund, on_delete=models.RESTRICT, null=True)


class CashRecept(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Payer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CashReceiptItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

