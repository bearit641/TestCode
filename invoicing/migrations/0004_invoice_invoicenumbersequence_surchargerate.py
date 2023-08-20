# Generated by Django 3.1.3 on 2021-07-29 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_contractnumber'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoicing', '0003_auto_20210624_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceNumberSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
            options={
                'db_table': 'invoice_number_sequence',
            },
        ),
        migrations.CreateModel(
            name='SurchargeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('courier', models.CharField(default='', max_length=255)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.zohoclient')),
            ],
            options={
                'db_table': 'surcharge_rate',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('filename', models.CharField(max_length=255)),
                ('invoice_number', models.CharField(max_length=255)),
                ('contract_number', models.IntegerField()),
                ('billing_filename', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('date_invoiced', models.DateField(null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.zohoclient')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoicing_invoice_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoicing_invoice_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoicing_invoice_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'invoices',
            },
        ),
    ]
