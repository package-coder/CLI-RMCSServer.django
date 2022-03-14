from urllib import request
from django.utils import timezone
from django.db import models
from accounts.models import User
import uuid
# Create your models here.

#TODO: REQUEST - Purchase Transaction Type > Entries
#FINISHED TODO: REQUEST - same values to TRANSACTION
#TODO: ITEM - Adding to inventory


class AFPrefix(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=100)


class AFTransactionStatus(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=100)


class AFTransactionType(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=50)


class AFType(models.Model):
    form_number = models.IntegerField()
    title = models.CharField(max_length=100)
    series_length = models.IntegerField()
    use_type = models.CharField(max_length=50, null=True)
    unit = models.CharField(max_length=25, default='STUB')
    quantity = models.IntegerField(default=1)


class AFState(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=100)


class AFPersonTransactionRecord(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    

class AFRequestHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(User, on_delete=models.RESTRICT)
    prefix = models.ForeignKey(AFPrefix, on_delete=models.RESTRICT, default='PREFIX_REQUEST')
    status = models.ForeignKey(AFTransactionStatus, on_delete=models.RESTRICT, default='STATUS_PENDING')
    request_type = models.ForeignKey(AFTransactionType, on_delete=models.RESTRICT)
    control_number = models.IntegerField(default=1)
    request_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self._state.adding:
            control_number = AFRequestHistory.objects.all().aggregate(largest=models.Max('control_number'))['largest']

            if control_number is not None:
                self.control_number = control_number + 1

        super(AFRequestHistory, self).save(*args, **kwargs)

class AFRequestItem(models.Model):
    af_type = models.ForeignKey(AFType, on_delete=models.RESTRICT)
    request_history = models.ForeignKey(AFRequestHistory, on_delete=models.RESTRICT, null=True)
    quantity = models.IntegerField(default=1)


class AFTransactionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issued_to = models.ForeignKey(AFPersonTransactionRecord, on_delete=models.RESTRICT)
    operator = models.ForeignKey(User, on_delete=models.RESTRICT)
    transaction_type = models.ForeignKey(AFTransactionType, on_delete=models.RESTRICT)
    request_history = models.ForeignKey(AFRequestHistory, on_delete=models.RESTRICT, null=True)
    prefix = models.ForeignKey(AFPrefix, on_delete=models.RESTRICT, default='PREFIX_TRANSACTION')
    status = models.ForeignKey(AFTransactionStatus, on_delete=models.RESTRICT, default='STATUS_PENDING')
    control_number = models.IntegerField(default=1)
    issued_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self._state.adding:
            control_number = AFTransactionHistory.objects.all().aggregate(largest=models.Max('control_number'))['largest']

            if control_number is not None:
                self.control_number = control_number + 1

        super(AFTransactionHistory, self).save(*args, **kwargs)


class AFTransactionItem(models.Model):
    af_type = models.ForeignKey(AFType, on_delete=models.RESTRICT)
    request_item = models.ForeignKey(AFRequestItem, on_delete=models.RESTRICT, null=True)
    transaction_history = models.ForeignKey(AFTransactionHistory, on_delete=models.RESTRICT, null=True)
    quantity = models.IntegerField(default=1)


class AFInventory(models.Model):
    pass


class AFItem(models.Model):
    af_type = models.ForeignKey(AFType, on_delete=models.RESTRICT)
    start_series = models.IntegerField()
    current_series = models.IntegerField()
    end_series = models.IntegerField()
    stub_number = models.IntegerField()
    active = models.BooleanField()
    prefix = models.CharField(max_length=10, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)

class AFPurchaseTransactionItem(models.Model):
    transaction_item = models.ForeignKey(AFTransactionItem, on_delete=models.RESTRICT, null=True)
    start_series = models.IntegerField()
    end_series = models.IntegerField()
    stub_number = models.IntegerField()
    prefix = models.CharField(max_length=10, blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)