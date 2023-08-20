from django.db import models

from core.models import BaseModel


class Invoice(BaseModel):
    """
    Storage for invoice records.
    """
    class Meta:
        db_table = 'invoices'

    filename = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=255)
    contract_number = models.IntegerField()
    client = models.ForeignKey(
        'clients.ZohoClient',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    billing_filename = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date_invoiced = models.DateField(null=True)


class InvoiceNumberSequence(models.Model):
    """
    A model where the invoice sequence number will be stored.
    """

    class Meta:
        db_table = 'invoice_number_sequence'

    number = models.IntegerField()


class SurchargeRate(models.Model):
    """
    A model where surcharges rate are stored.
    These rates are used in invoice generation.
    """

    class Meta:
        db_table = 'surcharge_rate'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    original_code = models.CharField(max_length=255, default='')
    rate = models.DecimalField(
        default=0,
        max_digits=20,
        decimal_places=2
    )
    client = models.ForeignKey(
        'clients.ZohoClient',
        on_delete=models.CASCADE
    )
    courier = models.CharField(
        max_length=255,
        default=''
    )


class ParcelServices(BaseModel):
    """
    Storage for Parcel Services records.
    """
    class Meta:
        db_table = 'parcel_services'
        indexes = [
            models.Index(
                fields=['id'],
                name='dc_service_id_index'
            )
        ]
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class ParcelWeightClasses(BaseModel):
    """
    Storage for Parcel Weight Class records.
    """
    class Meta:
        db_table = 'parcel_weight_class'
        indexes = [
            models.Index(
                fields=['id'],
                name='dc_weight_class_id_index'
            )
        ]

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    min_weight = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2
    )
    max_weight = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2
    )
    service_id = models.PositiveIntegerField(default=0)


class ParcelZones(BaseModel):
    """
    Storage for Parcel Zones records.
    """
    class Meta:
        db_table = 'parcel_zones'
        indexes = [
            models.Index(
                fields=['zone_id'],
                name='dc_parcel_zone_id_index'
            )
        ]

    zone_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    post_codes = models.CharField(max_length=255, default='')
    service_id = models.PositiveIntegerField(default=0)
    iso = models.CharField(max_length=5, default='')


class ParcelSalePrice(BaseModel):
    """
    Storage for Parcel Sale Price records.
    """
    class Meta:
        db_table = 'parcel_sale_price'
        indexes = [
            models.Index(
                fields=['client_number'],
                name='dc_sale_client_idx'
            ),
            models.Index(
                fields=['courier'],
                name='dc_sale_courier_idx'
            )
        ]
    client_number = models.PositiveIntegerField()
    courier = models.CharField(max_length=255)
    service = models.ForeignKey(ParcelServices, on_delete=models.CASCADE)
    zone_id = models.PositiveIntegerField(default=0)
    weight_class = models.ForeignKey(
        ParcelWeightClasses,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2
    )


class ParcelCostPrice(BaseModel):
    """
    Storage for Parcel Cost Price records.
    """
    class Meta:
        db_table = 'parcel_cost_price'
        indexes = [
            models.Index(
                fields=['courier'],
                name='dc_cost_courier_idx'
            )
        ]
    courier = models.CharField(max_length=255)
    service = models.ForeignKey(ParcelServices, on_delete=models.CASCADE)
    zone_id = models.PositiveIntegerField(default=0)
    weight_class = models.ForeignKey(
        ParcelWeightClasses,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2
    )
