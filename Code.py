import json
from datetime import datetime
from datetime import timedelta

import requests
from braces.views import JSONResponseMixin

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic import View

from clients.models import ZohoClient
from core.aws_functions import create_presigned_url
from core.aws_functions import list_s3_bucket_objects
from core.aws_functions import publish_sns
from core.aws_functions import save_bytes_to_s3
from core.logs_handler import logger
from despatch_cloud.mixins import CSVResponseMixin
from users.models import Profile
from .forms import BillingFileForm
from .forms import CostForm
from .forms import SalesForm
from .forms import ServiceForm
from .forms import SurchargeRatesForm
from .forms import WeightClassForm
from .forms import ZoneForm
from .models import Invoice
from .models import ParcelCostPrice
from .models import ParcelSalePrice
from .models import ParcelServices
from .models import SurchargeRate
from .models import ParcelWeightClasses
from .models import ParcelZones


class UploadBillingFileView(
        LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, FormView):
    """
    Formview for Billing File Upload page.
    """

    template_name = 'invoicing.html'
    form_class = BillingFileForm
    success_message = 'Billing File is being processed.'
    success_url = reverse_lazy('invoicing:list')

   

    def test_func(self):
        return (
            self.request.user.profiles.role == Profile.ADMIN_ROLE
            or self.request.user.profiles.role == Profile.ACCOUNTING_ROLE
        )

    def form_valid(self, form):
        filename = form.cleaned_data['billing_file'].name
        file_content = form.cleaned_data['billing_file'].read()

        # Save the file in AWS S3 bucket for billing file.
        save_bytes_to_s3(
            file_content,
            filename,
            settings.AWS_BUCKETS['BILLING_FILE_BUCKET_NAME']
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billing_files'] = list_s3_bucket_objects(
            settings.AWS_BUCKETS['BILLING_FILE_BUCKET_NAME']
        )
        invoice_covered_date = (
            timezone.now().date() - timedelta(days=60)
        )
        context['invoices'] = Invoice.objects.filter(
            datetime_created__gt=invoice_covered_date
        )
        return context


class DownloadBillingFileView(LoginRequiredMixin, View):
    """
    A view that will download billing files from s3 bucket.
    """

    def get(self, *args, **kwargs):
        filename = self.kwargs['filename']
        url = create_presigned_url(
            settings.AWS_BUCKETS['BILLING_FILE_BUCKET_NAME'],
            filename
        )
        return redirect(url)


class DownloadInvoiceView(LoginRequiredMixin, View):
    """
    A view that will download invoices from s3 bucket.
    """

    def get(self, *args, **kwargs):
        filename = self.kwargs['filename']
        url = create_presigned_url(
            settings.AWS_BUCKETS['INVOICE_BUCKET_NAME'],
            filename
        )
        return redirect(url)


class SendInvoiceView(LoginRequiredMixin, JSONResponseMixin, View):
    """
    A view that will send a request to our API Gateway
    to send the invoice to the client.
    """

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        invoice_id = self.request.POST.get('invoice_id')
        invoice = Invoice.objects.get(pk=invoice_id)

        headers = {
            'x-api-key': settings.SEND_INVOICE_API_KEY,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        payload = {
            'email': email,
            'filename': invoice.filename,
            'invoice_number': invoice.invoice_number,
            'contract_number': invoice.contract_number,
            'client': invoice.client.client_name,
            'formatted_invoice_date': invoice.date_invoiced.strftime('%b %d, %Y')
        }

        url = settings.SEND_INVOICE_ENDPOINT
        response = requests.request(
            'POST',
            url,
            headers=headers,
            data=json.dumps(payload)
        )
        status = 200
        data = {
            'status': 200,
            'status_message': 'success' 
        }
        if response.status_code != 200:
            data['status'] = response.status_code
            data['status_message'] = 'error'
        return self.render_json_response(data, data['status'])


class SurchargeRatesFormView(
    LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    Formview for Surcharge Rate File Upload page.
    """

    template_name = 'invoice_rates.html'
    form_class = SurchargeRatesForm
    success_message = 'Surcharge Rate File is being processed.'
    success_url = reverse_lazy('invoicing:rates')

    def form_valid(self, form):
        filename = form.cleaned_data['surcharge_rate_file'].name
        file_content = form.cleaned_data['surcharge_rate_file'].read()
        logger.info(f'Got surcharge file {filename}')

        bucket_name = settings.AWS_BUCKETS['RATES_UPDATE_BUCKET_NAME']
        # Save the file in AWS S3 bucket for surcharge file.
        save_bytes_to_s3(
            file_content,
            filename,
            bucket_name
        )

        message = json.dumps({
            'event': 'surcharge',
            'bucket_name': bucket_name,
            'filename': filename
        })
        try:
            publish_sns(
                'arn:aws:sns:eu-west-1:631490976110:rates-update-topic',
                'Rates Update',
                message
            )
            logger.info(f'Sent sns to rates-topic.')
        except Exception as e:
            logger.warning(
                f'Failed to send sns to rates-topic. {e}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = SurchargeRate.objects.all()
        return context


class SurchargeRatesExportView(CSVResponseMixin, View):
    """
    View for exporting Surcharge Rates data into a CSV file.
    """

    def __init__(self):
        super().__init__()
        self.clients = {
            client.id: client.client_name
            for client in ZohoClient.objects.all()
        }

    def get_queryset(self, **filter_kwargs):
        """
        Return the data needed.
        """

        queryset = (
            SurchargeRate.objects
            .all()
            .order_by('code')
            .values(
                'code',
                'original_code',
                'name',
                'courier',
                'client',
                'rate'
            )
        )
        return queryset

    def get(self, *args, **kwargs):

        csv_content_header = [
            'Code',
            'Original Code',
            'Name',
            'Courier',
            'Client',
            'Rate'
        ]
        rates = self.get_queryset()
        csv_content = [csv_content_header]
        for rate in rates:
            csv_content.append(
                [
                    rate['code'],
                    rate['original_code'],
                    rate['name'],
                    rate['courier'],
                    self.clients.get(rate['client'], ''),
                    rate['rate']
                ]
            )
        context = {
            'file_name': f'surcharge-rates_{datetime.today()}',
            'csv_content': csv_content
        }
        return self.render_to_response(context)


class ServiceFormView(
    LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    Formview for Service File Upload page.
    """

    template_name = 'service_list.html'
    form_class = ServiceForm
    success_message = 'Service File is being processed.'
    success_url = reverse_lazy('invoicing:service')

    def form_valid(self, form):
        filename = form.cleaned_data['service_file'].name
        file_content = form.cleaned_data['service_file'].read()
        logger.info(f'Got service file {filename}')

        bucket_name = settings.AWS_BUCKETS['RATES_UPDATE_BUCKET_NAME']
        # Save the file in AWS S3 bucket for service file.
        logger.info(f'Saving {filename} to {bucket_name}')
        save_bytes_to_s3(
            file_content,
            filename,
            bucket_name
        )

        message = json.dumps({
            'event': 'service',
            'bucket_name': bucket_name,
            'filename': filename
        })
        try:
            publish_sns(
                'arn:aws:sns:eu-west-1:631490976110:rates-update-topic',
                'Rates Update',
                message
            )
            logger.info(f'Sent sns to rates-topic.')
        except Exception as e:
            logger.warning(
                f'Failed to send sns to rates-topic. {e}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = ParcelServices.objects.all()
        return context


class ServiceExportView(CSVResponseMixin, View):
    """
    View for exporting Service data into a CSV file.
    """

    def get_queryset(self, **filter_kwargs):
        """
        Return the data needed.
        """

        queryset = (
            ParcelServices.objects
            .all()
            .order_by('id')
            .values(
                'id',
                'code',
                'name'
            )
        )
        return queryset

    def get(self, *args, **kwargs):

        csv_content_header = [
            'service_id',
            'service_code',
            'service_name'
        ]
        rates = self.get_queryset()
        csv_content = [csv_content_header]
        for rate in rates:
            csv_content.append(
                [
                    rate['id'],
                    rate['code'],
                    rate['name']
                ]
            )
        context = {
            'file_name': f'service_{datetime.today()}',
            'csv_content': csv_content
        }
        return self.render_to_response(context)


class WeightClassFormView(
    LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    Formview for Weight Class File Upload page.
    """

    template_name = 'weight_list.html'
    form_class = WeightClassForm
    success_message = 'Weight class File is being processed.'
    success_url = reverse_lazy('invoicing:weight_class')

    def form_valid(self, form):
        filename = form.cleaned_data['weight_class_file'].name
        file_content = form.cleaned_data['weight_class_file'].read()
        logger.info(f'Got weight class file {filename}')

        bucket_name = settings.AWS_BUCKETS['RATES_UPDATE_BUCKET_NAME']
        logger.info(f'Saving {filename} to {bucket_name}')
        # Save the file in AWS S3 bucket for weight class file.
        save_bytes_to_s3(
            file_content,
            filename,
            bucket_name
        )

        message = json.dumps({
            'event': 'weight_class',
            'bucket_name': bucket_name,
            'filename': filename
        })
        try:
            publish_sns(
                'arn:aws:sns:eu-west-1:631490976110:rates-update-topic',
                'Rates Update',
                message
            )
            logger.info(f'Sent sns to rates-topic.')
        except Exception as e:
            logger.warning(
                f'Failed to send sns to rates-topic. {e}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weight_classes'] = ParcelWeightClasses.objects.all()
        return context


class WeightClassExportView(CSVResponseMixin, View):
    """
    View for exporting weight class data into a CSV file.
    """

    def get_queryset(self, **filter_kwargs):
        """
        Return the data needed.
        """

        queryset = (
            ParcelWeightClasses.objects
            .all()
            .order_by('id')
            .values(
                'id',
                'name',
                'service_id',
                'min_weight',
                'max_weight'
            )
        )
        return queryset

    def get(self, *args, **kwargs):

        csv_content_header = [
            'weight_class_id',
            'weight_class_name',
            'service_id',
            'min_weight',
            'max_weight'
        ]
        weights = self.get_queryset()
        csv_content = [csv_content_header]
        for weight in weights:
            csv_content.append(
                [
                    weight['id'],
                    weight['name'],
                    weight['service_id'],
                    weight['min_weight'],
                    weight['max_weight']
                ]
            )
        context = {
            'file_name': f'weight-class_{datetime.today()}',
            'csv_content': csv_content
        }
        return self.render_to_response(context)


class ZoneFormView(
    LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    Formview for Zone File Upload page.
    """

    template_name = 'zone_list.html'
    form_class = ZoneForm
    success_message = 'Zone File is being processed.'
    success_url = reverse_lazy('invoicing:zone')

    def form_valid(self, form):
        filename = form.cleaned_data['zone_file'].name
        file_content = form.cleaned_data['zone_file'].read()
        logger.info(f'Got zone file {filename}')

        bucket_name = settings.AWS_BUCKETS['RATES_UPDATE_BUCKET_NAME']
        logger.info(f'Saving {filename} to {bucket_name}')
        # Save the file in AWS S3 bucket for zone file.
        save_bytes_to_s3(
            file_content,
            filename,
            bucket_name
        )

        message = json.dumps({
            'event': 'zone',
            'bucket_name': bucket_name,
            'filename': filename
        })
        try:
            publish_sns(
                'arn:aws:sns:eu-west-1:631490976110:rates-update-topic',
                'Rates Update',
                message
            )
            logger.info(f'Sent sns to rates-topic.')
        except Exception as e:
            logger.warning(
                f'Failed to send sns to rates-topic. {e}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zones'] = ParcelZones.objects.all()
        return context


class ZoneExportView(CSVResponseMixin, View):
    """
    View for exporting zone data into a CSV file.
    """

    def get_queryset(self, **filter_kwargs):
        """
        Return the data needed.
        """

        queryset = (
            ParcelZones.objects
            .all()
            .order_by('zone_id')
            .values(
                'name',
                'service_id',
                'post_codes',
                'iso',
                'zone_id'
            )
        )
        return queryset

    def get(self, *args, **kwargs):

        csv_content_header = [
            'zone_id',
            'zone_name',
            'iso',
            'service_id',
            'post_codes'
        ]
        zones = self.get_queryset()
        csv_content = [csv_content_header]
        for zone in zones:
            csv_content.append(
                [
                    zone['zone_id'],
                    zone['name'],
                    zone['iso'],
                    zone['service_id'],
                    zone['post_codes']
                ]
            )
        context = {
            'file_name': f'zone_{datetime.today()}',
            'csv_content': csv_content
        }
        return self.render_to_response(context)


class CostFormView(
    LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    Formview for Cost File Upload page.
    """

    template_name = 'cost_list.html'
    form_class = CostForm
    success_message = 'Cost File is being processed.'
    success_url = reverse_lazy('invoicing:cost')

    def form_valid(self, form):
        filename = form.cleaned_data['cost_file'].name
        file_content = form.cleaned_data['cost_file'].read()

        bucket_name = settings.AWS_BUCKETS['RATES_UPDATE_BUCKET_NAME']
        logger.info(f'Saving {filename} to {bucket_name}')
        # Save the file in AWS S3 bucket for cost file.
        save_bytes_to_s3(
            file_content,
            filename,
            bucket_name
        )

        message = json.dumps({
            'event': 'cost',
            'bucket_name': bucket_name,
            'filename': filename
        })
        try:
            publish_sns(
                'arn:aws:sns:eu-west-1:631490976110:rates-update-topic',
                'Rates Update',
                message
            )
            logger.info(f'Sent sns to rates-topic.')
        except Exception as e:
            logger.warning(
                f'Failed to send sns to rates-topic. {e}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costs'] = ParcelCostPrice.objects.all()
        return context


class CostExportView(CSVResponseMixin, View):
    """
    View for exporting cost data into a CSV file.
    """

    def get_queryset(self, **filter_kwargs):
        """
        Return the data needed.
        """

        queryset = (
            ParcelCostPrice.objects
            .all()
            .order_by('service_id')
            .values(
                'courier',
                'service_id',
                'weight_class_id',
                'zone_id',
                'price'
            )
        )
        return queryset

    def get(self, *args, **kwargs):

        csv_content_header = [
            'courier_code',
            'service_id',
            'weight_class_id',
            'zone_id',
            'price'
        ]
        costs = self.get_queryset()
        csv_content = [csv_content_header]
        for cost in costs:
            csv_content.append(
                [
                    cost['courier'],
                    cost['service_id'],
                    cost['weight_class_id'],
                    cost['zone_id'],
                    cost['price']
                ]
            )
        context = {
            'file_name': f'cost_{datetime.today()}',
            'csv_content': csv_content
        }
        return self.render_to_response(context)


class SalesFormView(
    LoginRequiredMixin, SuccessMessageMixin, FormView):

    """
    Formview for Sales File Upload page.
    """

    template_name = 'sales_list.html'
    form_class = SalesForm
    success_message = 'Sales File is being processed.'
    success_url = reverse_lazy('invoicing:sales')

    def form_valid(self, form):
        filename = form.cleaned_data['sales_file'].name
        file_content = form.cleaned_data['sales_file'].read()

        bucket_name = settings.AWS_BUCKETS['RATES_UPDATE_BUCKET_NAME']
        logger.info(f'Saving {filename} to {bucket_name}')
        # Save the file in AWS S3 bucket for sales file.
        save_bytes_to_s3(
            file_content,
            filename,
            bucket_name
        )

        message = json.dumps({
            'event': 'sales',
            'bucket_name': bucket_name,
            'filename': filename
        })
        try:
            publish_sns(
                'arn:aws:sns:eu-west-1:631490976110:rates-update-topic',
                'Rates Update',
                message
            )
            logger.info(f'Sent sns to rates-topic.')
        except Exception as e:
            logger.warning(
                f'Failed to send sns to rates-topic. {e}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = ParcelSalePrice.objects.all()
        return context


class SalesExportView(CSVResponseMixin, View):
    """
    View for exporting sales data into a CSV file.
    """

    def __init__(self):
        super().__init__()
        self.clients = {
            client.id: client.client_name
            for client in ZohoClient.objects.all()
        }

    def get_queryset(self, **filter_kwargs):
        """
        Return the data needed.
        """

        queryset = (
            ParcelSalePrice.objects
            .all()
            .order_by('client_number')
            .values(
                'client_number',
                'courier',
                'service_id',
                'weight_class_id',
                'zone_id',
                'price'
            )
        )
        return queryset

    def get(self, *args, **kwargs):

        csv_content_header = [
            'client_number',
            'client_name',
            'courier',
            'service_id',
            'weight_class_id',
            'zone_id',
            'price'
        ]
        sales = self.get_queryset()
        csv_content = [csv_content_header]
        for sale in sales:
            csv_content.append(
                [
                    sale['client_number'],
                    self.clients.get(sale['client_number'], ''),
                    sale['courier'],
                    sale['service_id'],
                    sale['weight_class_id'],
                    sale['zone_id'],
                    sale['price']
                ]
            )
        context = {
            'file_name': f'sales_{datetime.today()}',
            'csv_content': csv_content
        }
        return self.render_to_response(context)


def handler500(request):
    return render(request, '500.html', status=500)
   #print(request)
