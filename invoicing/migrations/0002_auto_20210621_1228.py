# Generated by Django 3.1.3 on 2021-06-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcelweightclasses',
            name='service_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parcelzones',
            name='iso',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='parcelzones',
            name='service_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]