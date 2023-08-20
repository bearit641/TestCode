import json

from datetime import datetime
from datetime import timedelta

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from clients.models import ZohoClient
from core.shortcuts import get_object_or_None
from users.models import Profile

from .forms import DashboardFilterForm
from .forms import RevenueFilterForm


class FrontPageBaseTemplateView(LoginRequiredMixin, TemplateView):
    """
    Template for front page. View will contains tracking functions
    and details about the HubEurope.
    """
    template_name = 'dashboard/frontpage.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user'] = self.request.user
        return self.render_to_response(context)


class DashboardBaseTemplateView(LoginRequiredMixin, TemplateView):
    """
    Template for dashboard home page. View will contain a lot of aggregation
    functions for charting and summarizing data. As such, view forms will
    limited to filtering functions.
    """
    template_name = 'dashboard/aggregations.html'

    def get_context_data(self, **kwargs):
        context = {}
        # Default start and end date range is 30 days.
        start_date = timezone.now() - timedelta(days=30)
        end_date = timezone.now()
        client = None
        if self.request.user.profiles.role == Profile.CLIENT_ROLE:
            client = get_object_or_None(
                ZohoClient, pk=self.request.user.profiles.client_id
            )
        courier = ''

        if self.request.GET.get('start_date'):
            start_date = datetime.strptime(
                self.request.GET.get('start_date'),
                '%Y-%m-%d'
            )
        if self.request.GET.get('end_date'):
            end_date = datetime.strptime(
                self.request.GET.get('end_date'),
                '%Y-%m-%d'
            )
        if self.request.GET.get('client'):

            client = get_object_or_None(
                ZohoClient, pk=self.request.GET.get('client')
            )

        if self.request.GET.get('courier'):
            courier = self.request.GET.get('courier')

        initial = {'start_date': start_date, 'end_date': end_date}
        if client:
            initial.update({'client': client})
        if courier:
            initial.update({'courier': courier})
        context['filter_form'] = DashboardFilterForm(
            profile=self.request.user.profiles, initial=initial
        )
        context['revenue_form'] = (
            RevenueFilterForm(
                {
                    'revenue_start_date': timezone.now(),
                    'revenue_end_date': timezone.now()
                }
            )
        )

        context['start_date'] = start_date
        context['end_date'] = end_date
        context['selected_client'] = client if client else None
        context['courier'] = courier

        clients = {}
        for client in ZohoClient.objects.all():
            clients.update({str(client.client_number): client.client_name})
        context['clients'] = json.dumps(clients)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user'] = self.request.user
        return self.render_to_response(context)


def handler403(request):
    return render(request, '403.html', status=403)


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
