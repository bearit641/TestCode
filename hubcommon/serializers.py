from rest_framework.serializers import ModelSerializer

from .models import Address


class AddressSerializer(ModelSerializer):
    """
    The serializer class for Address model.
    """

    class Meta:
        model = Address
        fields = '__all__'
