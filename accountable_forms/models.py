from django.db import models
import uuid
# Create your models here.


class AFType(models.Model):
    form_number = models.IntegerField()
    title = models.CharField(max_length=50)
    series_length = models.IntegerField(null=True)
    use_type = models.CharField(max_length=50, null=True)
    unit = models.CharField(max_length=25, default='STUB')
    quantity = models.IntegerField(default=1)

    REQUIRED_FIELDS = ['form_number', 'title']

class AFRequestHistory(models.Model):
    prefix = models.CharField(max_length=10)
    control_number = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    date_filed = models.DateField()
    request_type = models.CharField(max_length=50)
    requester_id = models.CharField(max_length=50)
    requester_name = models.CharField(max_length=255)

class AFRequestItem(models.Model):
    af_type = models.ForeignKey(AFType, on_delete=models.RESTRICT)
    request = models.ForeignKey(AFRequestHistory, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)

    REQUIRED_FIELDS = ['af_type', 'request']

class AFTransactionItem(models.Model):
    pass


class AFTransactionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_id = models.ForeignKey(AFRequestHistory, on_delete=models.DO_NOTHING)
    prefix = models.CharField(max_length=10)
    control_number = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    date_filed = models.DateField()
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=255)
    issued_id = models.CharField(max_length=50)
    issued_name = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=50)