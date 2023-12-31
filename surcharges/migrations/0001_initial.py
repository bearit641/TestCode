# Generated by Django 3.1.3 on 2021-02-22 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Surcharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('courier', models.CharField(max_length=255)),
                ('service_code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='surcharges_surcharge_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='surcharges_surcharge_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='surcharges_surcharge_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'surcharges',
            },
        ),
        migrations.CreateModel(
            name='ClientSurcharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.CharField(max_length=255)),
                ('barcode', models.CharField(max_length=255)),
                ('reference_number', models.CharField(max_length=255)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('invoice_date', models.DateField()),
                ('invoice_file', models.FileField(blank=True, null=True, upload_to='')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='surcharges_clientsurcharge_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='surcharges_clientsurcharge_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('surcharge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='surcharges.surcharge')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='surcharges_clientsurcharge_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'client_surcharges',
            },
        ),
        migrations.AddIndex(
            model_name='surcharge',
            index=models.Index(fields=['courier'], name='surcharges_courier_34f01d_idx'),
        ),
        migrations.AddIndex(
            model_name='clientsurcharge',
            index=models.Index(fields=['client'], name='client_surc_client_2b2f1a_idx'),
        ),
        migrations.AddIndex(
            model_name='clientsurcharge',
            index=models.Index(fields=['barcode'], name='client_surc_barcode_156cb7_idx'),
        ),
        migrations.AddIndex(
            model_name='clientsurcharge',
            index=models.Index(fields=['invoice_date'], name='client_surc_invoice_0e7761_idx'),
        ),
    ]
