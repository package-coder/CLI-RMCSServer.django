# Generated by Django 4.0.2 on 2022-03-08 04:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accountable_forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afrequesthistory',
            name='control_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='afrequesthistory',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='aftransactionhistory',
            name='control_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='aftransactionhistory',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
