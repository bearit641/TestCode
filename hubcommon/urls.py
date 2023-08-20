from django.urls import path, include

from hubeurope.urls import router
from .views import AddressViewSet


app_name = 'hubcommon'

router.register('addresses', AddressViewSet, 'addresses')

urlpatterns = []
