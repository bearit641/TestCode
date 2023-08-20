from django.urls import path

from .views import ClientSurchargeListView
from .views import SurchargeListView

app_name = 'surcharges'

urlpatterns = [
    path(
        '',
        SurchargeListView.as_view(),
        name='list-surcharges'
    ),
    path(
        'client',
        ClientSurchargeListView.as_view(),
        name='list-client-surcharges'
    )
]
