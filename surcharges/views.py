import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import ClientSurcharge
from .models import Surcharge


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SurchargeListView(LoginRequiredMixin, ListView):
    """
    Renders list of surcharges objects.
    """
    queryset = Surcharge.objects.order_by('-datetime_created')
    paginate_by = 20


class ClientSurchargeListView(LoginRequiredMixin, ListView):
    """
    Renders list of Client surcharges objects.
    """
    queryset = ClientSurcharge.objects.order_by('-datetime_created')
    paginate_by = 20
