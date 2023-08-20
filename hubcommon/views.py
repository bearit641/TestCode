from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(ReadOnlyModelViewSet):
    """
    This view will contain functions to process postcode addresses.
    """

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        """
        This function will return the address of the given postcode.
        """

        postcode = self.request.GET.get('postcode')
        query_set = super().get_queryset()

        if postcode:
            query_set = query_set.filter(
                postcode=postcode
            )
        return query_set
