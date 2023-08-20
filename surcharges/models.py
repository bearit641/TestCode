from django.db import models

from core.models import BaseModel


class Surcharge(BaseModel):
    """
    Storage for surchages per courier.
    """
    courier = models.CharField(max_length=255)
    service_code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'surcharges'
        indexes = [
            models.Index(fields=['courier']),
        ]


class ClientSurcharge(BaseModel):
    """
    Items that were billed differently because of various reason.
    Ex. Reprint, Return to Seller, and etc.
    """
    surcharge = models.ForeignKey(
        Surcharge,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    client = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    invoice_date = models.DateField()
    invoice_file = models.FileField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'client_surcharges'
        indexes = [
            models.Index(fields=['client']),
            models.Index(fields=['barcode']),
            models.Index(fields=['invoice_date'])
        ]
