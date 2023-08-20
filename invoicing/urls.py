from django.urls import path

from .views import CostExportView
from .views import CostFormView
from .views import DownloadBillingFileView
from .views import DownloadInvoiceView
from .views import SalesExportView
from .views import SalesFormView
from .views import SendInvoiceView
from .views import ServiceExportView
from .views import ServiceFormView
from .views import SurchargeRatesExportView
from .views import SurchargeRatesFormView
from .views import UploadBillingFileView
from .views import WeightClassExportView
from .views import WeightClassFormView
from .views import ZoneExportView
from .views import ZoneFormView

app_name = 'invoicing'

urlpatterns = [
    path(
        '',
        UploadBillingFileView.as_view(),
        name='list'
    ),

    path(
        'invoice/<str:filename>/download/',
        DownloadInvoiceView.as_view(),
        name='download'
    ),

    path(
        'invoice/send/',
        SendInvoiceView.as_view(),
        name='send_invoice'
    ),

    path(
        'file/<str:filename>/download/',
        DownloadBillingFileView.as_view(),
        name='billing_file_download'
    ),

    path(
        'rates/',
        SurchargeRatesFormView.as_view(),
        name='rates'
    ),

    path(
        'rates/export/',
        SurchargeRatesExportView.as_view(),
        name='surcharge_rates_export'
    ),

    path(
        'service/',
        ServiceFormView.as_view(),
        name='service'
    ),

    path(
        'service/export/',
        ServiceExportView.as_view(),
        name='service_export'
    ),

    path(
        'weight/',
        WeightClassFormView.as_view(),
        name='weight_class'
    ),

    path(
        'weight/export/',
        WeightClassExportView.as_view(),
        name='weight_class_export'
    ),

    path(
        'zone/',
        ZoneFormView.as_view(),
        name='zone'
    ),

    path(
        'zone/export/',
        ZoneExportView.as_view(),
        name='zone_export'
    ),

    path(
        'cost/',
        CostFormView.as_view(),
        name='cost'
    ),

    path(
        'cost/export/',
        CostExportView.as_view(),
        name='cost_export'
    ),

    path(
        'sales/',
        SalesFormView.as_view(),
        name='sales'
    ),

    path(
        'sales/export/',
        SalesExportView.as_view(),
        name='sales_export'
    )
]
