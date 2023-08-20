# Generated by Django 3.1.3 on 2021-06-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0002_auto_20210621_1228'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='parcelzones',
            name='dc_zone_id_index',
        ),
        migrations.AddField(
            model_name='parcelzones',
            name='zone_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='parcelzones',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddIndex(
            model_name='parcelzones',
            index=models.Index(fields=['zone_id'], name='dc_parcel_zone_id_index'),
        ),
    ]