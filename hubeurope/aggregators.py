from datetime import datetime
from datetime import timedelta

import pandas as pd

from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.utils import timezone

from clients.models import ZohoClient
from despatch_cloud.models import DespatchCloudRecord
from gardening_direct.models import GardeningDirectRecord


class DashboardAggregator(object):
    """
    A class that will contain the methods needed for the dashboard page.
    """

    gardening_direct_id = 101

    def __init__(self, **kwargs):
        client = kwargs.get('client')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.courier = kwargs.get('courier')
        self.client = client.client_number if client else None

    def get_daily_verification_context(self):
        """
        Returns the daily verification count for the date range.

        context = {
            'labels': ['May 1', May 2]
            'counts': [90, 10]
        }
        """

        context = {'labels': [], 'counts': []}
        start_date = self.start_date
        end_date = self.end_date + timedelta(days=1)
        filter_kwargs = {
            'datetime_verified__range': [start_date, end_date],
            'verified': True
        }

        if self.client:
            filter_kwargs.update({'customer_dc_id': self.client})
        if self.courier:
            filter_kwargs.update({'courier': self.courier})

        dates = [
            d.strftime('%B %d, %Y')
            for d in pd.date_range(self.start_date, self.end_date)
        ]

        gd_verified = (
            GardeningDirectRecord.objects.filter(**filter_kwargs)
            .exclude(datetime_verified__isnull=True)
            .annotate(date=TruncDate('datetime_verified'))
            .values('date')
            .annotate(Count('date'))
        )

        dc_verified = (
            DespatchCloudRecord.objects.filter(**filter_kwargs)
            .filter(verified=True)
            .exclude(datetime_verified__isnull=True)
            .annotate(date=TruncDate('datetime_verified'))
            .values('date')
            .annotate(Count('date'))
        )

        gd_verified_count = {
            record['date'].strftime('%B %d, %Y'): record['date__count']
            for record in gd_verified if record['date']
        }
        dc_verified_count = {
            record['date'].strftime('%B %d, %Y'): record['date__count']
            for record in dc_verified if record['date']
        }

        counts = []
        for date in dates:
            counts.append(
                dc_verified_count.get(date, 0)
                + gd_verified_count.get(date, 0)
            )

        context['labels'] = dates
        context['counts'] = counts
        return context

    def get_daily_label_request_context(self):
        """
        Returns the daily label count for the date range.

        context = {
            'labels': ['May 1', May 2]
            'counts': [90, 10]
        }
        """

        context = {'labels': [], 'counts': []}
        start_date = self.start_date
        end_date = self.end_date + timedelta(days=1)
        filter_kwargs = {
            'datetime_created__range': [start_date, end_date],
        }

        if self.client:
            filter_kwargs.update({'customer_dc_id': self.client})
        if self.courier:
            filter_kwargs.update({'courier': self.courier})

        dates = [
            d.strftime('%B %d, %Y')
            for d in pd.date_range(self.start_date, self.end_date)
        ]

        gd_labels = (
            GardeningDirectRecord.objects.filter(**filter_kwargs)
            .exclude(datetime_created__isnull=True)
            .annotate(date=TruncDate('datetime_created'))
            .values('date')
            .annotate(Count('date'))
        )

        dc_labels = (
            DespatchCloudRecord.objects.filter(**filter_kwargs)
            .exclude(Q(customer_dc_id=101) | Q(datetime_created__isnull=True))
            .annotate(date=TruncDate('datetime_created'))
            .values('date')
            .annotate(Count('date'))
        )

        gd_labels_count = {
            record['date'].strftime('%B %d, %Y'): record['date__count']
            for record in gd_labels if record['date']
        }
        dc_labels_count = {
            record['date'].strftime('%B %d, %Y'): record['date__count']
            for record in dc_labels if record['date']
        }

        counts = []
        for date in dates:
            counts.append(
                gd_labels_count.get(date, 0)
                + dc_labels_count.get(date, 0)
            )

        context['labels'] = dates
        context['counts'] = counts
        return context
