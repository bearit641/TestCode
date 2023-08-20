from datetime import date
from datetime import timedelta

from django.test import TestCase

from clients.models import ZohoClient

from ..models import Invoice
from ..models import InvoiceNumberSequence
from ..models import ParcelCostPrice
from ..models import ParcelSalePrice
from ..models import ParcelServices
from ..models import ParcelWeightClasses
from ..models import ParcelZones
from ..models import SurchargeRate


class InvoiceTestCase(TestCase):
    """
    A test script for testing Invoice model.
    """

    client_beerwulf_data = {
        'id': 1,
        'client_name': 'Beerwulf',
        'client_number': 301
    }

    client_etarget_data = {
        'id': 49,
        'client_name': 'ETarget Limited',
        'client_number': 656
    }

    test_beerwulf_data = {
        'filename': 'test_beerwulf_invoice.csv',
        'invoice_number': 'HEI-1234',
        'contract_number': 1234,
        'billing_filename': 'BILLINGFILE.csv',
        'status': 'Sent',
        'date_invoiced': date.today()
    }

    test_etarget_data = {
        'filename': 'test_etarget_invoice.csv',
        'invoice_number': 'HEI-5678',
        'contract_number': 5678,
        'billing_filename': 'BILLINGFILE.csv',
        'status': 'Sent',
        'date_invoiced': date.today()
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        self._create_client()
        self.test_beerwulf_data['client'] = ZohoClient.objects.get(pk=1)
        self.test_etarget_data['client'] = ZohoClient.objects.get(pk=49)
        try:
            Invoice.objects.create(
                **self.test_beerwulf_data
            )

            Invoice.objects.create(
                **self.test_etarget_data
            )
        except Exception as e:
            print(e)
    
    def _create_client(self):
        """
        Create a client data to be used in Invoice model.
        """
        try:
            ZohoClient.objects.create(**self.client_beerwulf_data)
            ZohoClient.objects.create(**self.client_etarget_data)
        except Exception as e:
            print(e)

    def test_get_beerwulf_invoice(self):
        """
        Test for getting specific invoice.
        """
        
        filter_kwargs = {
            'invoice_number': 'HEI-1234',
        }

        queried_invoice = (
            Invoice.objects.get(**filter_kwargs)
        )

        self.assertEqual(
            self.test_beerwulf_data['invoice_number'],
            queried_invoice.invoice_number
        )
        self.assertEqual(
            self.test_beerwulf_data['filename'],
            queried_invoice.filename
        )
        self.assertEqual(
            self.test_beerwulf_data['contract_number'],
            queried_invoice.contract_number
        )
        self.assertEqual(
            self.test_beerwulf_data['billing_filename'],
            queried_invoice.billing_filename
        )
        self.assertEqual(
            self.test_beerwulf_data['status'],
            queried_invoice.status
        )
        self.assertEqual(
            self.test_beerwulf_data['date_invoiced'],
            queried_invoice.date_invoiced
        )

    def test_get_invoices(self):
        """
        Test for getting all the invoices.
        """

        expected_output = {
            'count': 2,
        }

        invoices = Invoice.objects.all()
        self.assertEqual(
            expected_output['count'],
            invoices.count()
        )


class InvoiceNumberSequenceTestCase(TestCase):
    """
    A test script for testing InvoiceNumberSequence model.
    """

    test_invoice_number_sequence = {
        'id': 1,
        'number': 1
    }

    def setUp(self):
        """
        Initialize the test data.
        """

        try:
            InvoiceNumberSequence.objects.create(
                **self.test_invoice_number_sequence
            )

        except Exception as e:
            print(e)

    def test_get_invoice_number_sequence(self):
        """
        Test for getting the latest invoice number sequence.
        """

        latest_invoice_number = InvoiceNumberSequence.objects.latest('pk')
        self.assertEqual(
            self.test_invoice_number_sequence['number'],
            latest_invoice_number.number
        )


class SurchargeRateTestCase(TestCase):
    """
    A test script for testing SurchargeRate model.
    """

    test_surchage_rate = {
        'id': 1,
        'name': 'Home Return',
        'code': 'HAR',
        'original_code': 'HAR',
        'rate': 4.50,
        'courier': 'Yodel'
    }

    client_etarget_data = {
        'id': 49,
        'client_name': 'ETarget Limited',
        'client_number': 656
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        self._create_client()
        self.test_surchage_rate['client'] = ZohoClient.objects.get(pk=49)
        try:
            SurchargeRate.objects.create(
                **self.test_surchage_rate
            )

        except Exception as e:
            print(e)
    
    def _create_client(self):
        """
        Create a client data to be used in SurchageRate model.
        """
        try:
            ZohoClient.objects.create(**self.client_etarget_data)
        except Exception as e:
            print(e)

    def test_get_surchage_rate(self):
        """
        Test for getting the created surcharge rate.
        """
        
        queried_surcharge_rate = SurchargeRate.objects.get(pk=1)

        self.assertEqual(
            self.test_surchage_rate['name'],
            queried_surcharge_rate.name
        )
        self.assertEqual(
            self.test_surchage_rate['code'],
            queried_surcharge_rate.code
        )
        self.assertEqual(
            self.test_surchage_rate['original_code'],
            queried_surcharge_rate.original_code
        )
        self.assertEqual(
            self.test_surchage_rate['rate'],
            queried_surcharge_rate.rate
        )
        self.assertEqual(
            self.test_surchage_rate['client'],
            queried_surcharge_rate.client
        )
        self.assertEqual(
            self.test_surchage_rate['courier'],
            queried_surcharge_rate.courier
        )


class ParcelServicesTestCase(TestCase):
    """
    A test script for testing ParcelServices model.
    """

    test_parcel_service_data = {
        'id': 1,
        'code': 'test',
        'name': 'test'
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        try:
            ParcelServices.objects.create(
                **self.test_parcel_service_data
            )
        except Exception as e:
            print(e)

    def test_get_parcel_service(self):
        """
        Test for getting specific Parcel Service.
        """
        
        filter_kwargs = {
            'code': 'test',
        }

        queried_service = (
            ParcelServices.objects.get(**filter_kwargs)
        )

        self.assertEqual(
            self.test_parcel_service_data['code'],
            queried_service.code
        )
        self.assertEqual(
            self.test_parcel_service_data['name'],
            queried_service.name
        )


class ParcelWeightClassesTestCase(TestCase):
    """
    A test script for testing ParcelWeightClasses model.
    """

    test_parcel_weight_class_data = {
        'id': 1,
        'name': 'test',
        'min_weight': 1,
        'max_weight': 1,
        'service_id': 1
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        try:
            ParcelWeightClasses.objects.create(
                **self.test_parcel_weight_class_data
            )
        except Exception as e:
            print(e)

    def test_get_parcel_weight_class(self):
        """
        Test for getting specific Parcel Weight Class.
        """
        
        filter_kwargs = {
            'name': 'test',
        }

        queried_weight_class = (
            ParcelWeightClasses.objects.get(**filter_kwargs)
        )

        self.assertEqual(
            self.test_parcel_weight_class_data['name'],
            queried_weight_class.name
        )
        self.assertEqual(
            self.test_parcel_weight_class_data['min_weight'],
            queried_weight_class.min_weight
        )
        self.assertEqual(
            self.test_parcel_weight_class_data['max_weight'],
            queried_weight_class.max_weight
        )
        self.assertEqual(
            self.test_parcel_weight_class_data['service_id'],
            queried_weight_class.service_id
        )


class ParcelZonesTestCase(TestCase):
    """
    A test script for testing ParcelZones model.
    """

    test_parcel_zone_data = {
        'zone_id': 1,
        'name': 'test',
        'post_codes': 'test postcode',
        'service_id': 1,
        'iso': '12345'
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        try:
            ParcelZones.objects.create(
                **self.test_parcel_zone_data
            )
        except Exception as e:
            print(e)

    def test_get_parcel_zone(self):
        """
        Test for getting specific ParcelZones.
        """
        
        filter_kwargs = {
            'name': 'test',
        }

        queried_zone = (
            ParcelZones.objects.get(**filter_kwargs)
        )

        self.assertEqual(
            self.test_parcel_zone_data['zone_id'],
            queried_zone.zone_id
        )
        self.assertEqual(
            self.test_parcel_zone_data['name'],
            queried_zone.name
        )
        self.assertEqual(
            self.test_parcel_zone_data['post_codes'],
            queried_zone.post_codes
        )
        self.assertEqual(
            self.test_parcel_zone_data['service_id'],
            queried_zone.service_id
        )
        self.assertEqual(
            self.test_parcel_zone_data['iso'],
            queried_zone.iso
        )


class ParcelSalePriceTestCase(TestCase):
    """
    A test script for testing ParcelSalePrice model.
    """
    
    test_parcel_service_data = {
        'id': 1,
        'code': 'test',
        'name': 'test'
    }

    test_parcel_zone_data = {
        'zone_id': 1,
        'name': 'test',
        'post_codes': 'test postcode',
        'service_id': 1,
        'iso': '12345'
    }

    test_parcel_weight_class_data = {
        'id': 1,
        'name': 'test',
        'min_weight': 1,
        'max_weight': 1,
        'service_id': 1
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        self._create_service()
        self._create_zone()
        self._create_weight_class()

        try:
            self.test_parcel_sale_data = {
                'client_number': 1,
                'courier': 'Yodel',
                'service': ParcelServices.objects.get(id=1),
                'zone_id': 1,
                'weight_class': ParcelWeightClasses.objects.get(id=1),
                'price': 1.00,
            }
            ParcelSalePrice.objects.create(
                **self.test_parcel_sale_data
            )
        except Exception as e:
            print(e)
    
    def _create_service(self):
        """
        Create a Service test data.
        """
        try:
            ParcelServices.objects.create(**self.test_parcel_service_data)
        except Exception as e:
            print(e)
    
    def _create_zone(self):
        """
        Create a Zone test data.
        """
        try:
            ParcelZones.objects.create(**self.test_parcel_zone_data)
        except Exception as e:
            print(e)
    
    def _create_weight_class(self):
        """
        Create a Weight Class test data.
        """
        try:
            ParcelWeightClasses.objects.create(
                **self.test_parcel_weight_class_data
            )
        except Exception as e:
            print(e)

    def test_get_parcel_sale(self):
        """
        Test for getting specific Parcel Sale Price.
        """
        
        filter_kwargs = {
            'service__pk': 1,
            'zone_id': 1,
            'weight_class__pk': 1
        }

        queried_sale_price = (
            ParcelSalePrice.objects.get(**filter_kwargs)
        )

        self.assertEqual(
            self.test_parcel_sale_data['client_number'],
            queried_sale_price.client_number
        )
        self.assertEqual(
            self.test_parcel_sale_data['courier'],
            queried_sale_price.courier
        )
        self.assertEqual(
            self.test_parcel_sale_data['service'],
            queried_sale_price.service
        )
        self.assertEqual(
            self.test_parcel_sale_data['zone_id'],
            queried_sale_price.zone_id
        )
        self.assertEqual(
            self.test_parcel_sale_data['weight_class'],
            queried_sale_price.weight_class
        )
        self.assertEqual(
            self.test_parcel_sale_data['price'],
            queried_sale_price.price
        )


class ParcelCostPriceTestCase(TestCase):
    """
    A test script for testing ParcelCostPrice model.
    """
    
    test_parcel_service_data = {
        'id': 2,
        'code': 'test',
        'name': 'test'
    }

    test_parcel_zone_data = {
        'zone_id': 2,
        'name': 'test',
        'post_codes': 'test postcode',
        'service_id': 1,
        'iso': '12345'
    }

    test_parcel_weight_class_data = {
        'id': 2,
        'name': 'test',
        'min_weight': 1,
        'max_weight': 1,
        'service_id': 1
    }

    def setUp(self):
        """
        Initialize the test data.
        """
        self._create_service()
        self._create_zone()
        self._create_weight_class()

        try:
            self.test_parcel_cost_data = {
                'courier': 'Yodel',
                'service': ParcelServices.objects.get(id=2),
                'zone_id': 2,
                'weight_class': ParcelWeightClasses.objects.get(id=2),
                'price': 1.00,
            }
            ParcelCostPrice.objects.create(
                **self.test_parcel_cost_data
            )
        except Exception as e:
            print(e)
    
    def _create_service(self):
        """
        Create a Service test data.
        """
        try:
            ParcelServices.objects.create(**self.test_parcel_service_data)
        except Exception as e:
            print(e)
    
    def _create_zone(self):
        """
        Create a Zone test data.
        """
        try:
            ParcelZones.objects.create(**self.test_parcel_zone_data)
        except Exception as e:
            print(e)
    
    def _create_weight_class(self):
        """
        Create a Weight Class test data.
        """
        try:
            ParcelWeightClasses.objects.create(
                **self.test_parcel_weight_class_data
            )
        except Exception as e:
            print(e)

    def test_get_parcel_sale(self):
        """
        Test for getting specific Parcel Cost Price.
        """
        
        filter_kwargs = {
            'service__pk': 2,
            'zone_id': 2,
            'weight_class__pk': 2
        }

        queried_cost_price = (
            ParcelCostPrice.objects.get(**filter_kwargs)
        )

        self.assertEqual(
            self.test_parcel_cost_data['courier'],
            queried_cost_price.courier
        )
        self.assertEqual(
            self.test_parcel_cost_data['service'],
            queried_cost_price.service
        )
        self.assertEqual(
            self.test_parcel_cost_data['zone_id'],
            queried_cost_price.zone_id
        )
        self.assertEqual(
            self.test_parcel_cost_data['weight_class'],
            queried_cost_price.weight_class
        )
        self.assertEqual(
            self.test_parcel_cost_data['price'],
            queried_cost_price.price
        )
