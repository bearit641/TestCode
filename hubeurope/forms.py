from django import forms

from clients.models import ZohoClient
from despatch_cloud.models import DespatchCloudRecord
from users.models import Profile


class DashboardFilterForm(forms.Form):
    """
    A form use in the dashboard page for filtering.
    """

    # Get all the available couriers.
    couriers = (
        DespatchCloudRecord.objects
        .values_list('courier')
        .order_by('courier')
        .distinct()
    )

    # Add an empty value for the choices
    choices = (
        [('', '---------')] + [(courier[0], courier[0]) for courier in couriers]
    )

    start_date = forms.DateField(label='Start Date:')
    end_date = forms.DateField(label='End Date:')
    client = forms.ModelChoiceField(
        queryset=ZohoClient.objects.all().order_by('client_name'),
        required=False
    )
    courier = forms.ChoiceField(choices=choices, required=False)

    def __init__(self, profile, **kwargs):
        self.profile = profile
        super(DashboardFilterForm, self).__init__(**kwargs)
        if self.profile.role == Profile.CLIENT_ROLE:
            self.fields['client'].queryset = ZohoClient.objects.filter(
                pk=self.profile.client_id
            )


class RevenueFilterForm(forms.Form):
    """
    A form use in the dashboard page for filtering revenue chart.
    """

    revenue_start_date = forms.DateField(label='Start Date:')
    revenue_end_date = forms.DateField(label='End Date:')
    revenue_client = forms.ModelChoiceField(
        queryset=ZohoClient.objects.all().order_by('client_name'),
        required=False,
        label='Client:'
    )
