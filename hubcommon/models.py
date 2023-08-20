from django.db import models


class Address(models.Model):
    """
    The address class model.
    """

    postcode = models.CharField(max_length=12)
    posttown = models.CharField(max_length=32)
    district = models.CharField(max_length=24)
    locality = models.CharField(max_length=32)
    house_name = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    admin_county = models.CharField(max_length=32)

    class Meta:
        db_table = 'addresses'
        indexes = [
          models.Index(fields=['postcode']),
        ]
