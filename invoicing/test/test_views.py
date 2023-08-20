import json
from datetime import date
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from clients.models import ZohoClient
from users.models import Profile

TEST_USERNAME = 'unittest'
TEST_PASSWORD = 'all-test-failed'
User = get_user_model()


class UploadBillingFileViewTest(TestCase):
    """
    A test script for testing UploadBillingFileView.
    """

    client_beerwulf_data = {
        'id': 1,
        'client_name': 'Beerwulf',
        'client_number': 301
    }
    
    def setUp(self):
        """
        Initialize the test data.
        """
        try:
            self._create_user()
            self._create_client()
            self._create_profile()
            self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        except Exception as e:
            print(e)

    def _create_user(self):
        """
        Use to create a test user.
        """
        user = User()
        user.id = 1
        user.username = TEST_USERNAME
        user.set_password(TEST_PASSWORD)
        user.is_active = True
        user.save()
    
    def _create_client(self):
        """
        Create a test client data to be used in testing.
        """
        try:
            ZohoClient.objects.create(**self.client_beerwulf_data)
        except Exception as e:
            print(e)
    
    def _create_profile(self):
        """
        User to create a test profile.
        """
        profile = Profile()
        profile.user = User.objects.get(pk=1)
        profile.client = ZohoClient.objects.get(pk=1)
        profile.role = 'admin'
        profile.status = 'approved'
        profile.save()

    def test_get(self):
        """
        Test the url if it will return status 200.
        """

        url = f'/billing/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class DownloadBillingFileViewTest(TestCase):
    """
    A test script for testing DownloadBillingFileView.
    """

    client_beerwulf_data = {
        'id': 1,
        'client_name': 'Beerwulf',
        'client_number': 301
    }
    
    def setUp(self):
        """
        Initialize the test data.
        """
        try:
            self._create_user()
            self._create_client()
            self._create_profile()
            self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        except Exception as e:
            print(e)

    def _create_user(self):
        """
        Use to create a test user.
        """
        user = User()
        user.id = 1
        user.username = TEST_USERNAME
        user.set_password(TEST_PASSWORD)
        user.is_active = True
        user.save()
    
    def _create_client(self):
        """
        Create a test client data to be used in testing.
        """
        try:
            ZohoClient.objects.create(**self.client_beerwulf_data)
        except Exception as e:
            print(e)
    
    def _create_profile(self):
        """
        User to create a test profile.
        """
        profile = Profile()
        profile.user = User.objects.get(pk=1)
        profile.client = ZohoClient.objects.get(pk=1)
        profile.role = 'admin'
        profile.status = 'approved'
        profile.save()

    def test_get(self):
        """
        Test the url if it will return status 301.
        """

        url = f'/billing/file/G-A02874400585612_39025.csv/download'
        response = self.client.get(url)

        # This view will redirect user ti another URL to download the file
        # in the s3 bucket that's why we are expecting 301 status code.
        redirect_status = 301
        self.assertEqual(response.status_code, redirect_status)


class DownloadInvoiceViewTest(TestCase):
    """
    A test script for testing DownloadInvoiceView.
    """

    client_beerwulf_data = {
        'id': 1,
        'client_name': 'Beerwulf',
        'client_number': 301
    }
    
    def setUp(self):
        """
        Initialize the test data.
        """
        try:
            self._create_user()
            self._create_client()
            self._create_profile()
            self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        except Exception as e:
            print(e)

    def _create_user(self):
        """
        Use to create a test user.
        """
        user = User()
        user.id = 1
        user.username = TEST_USERNAME
        user.set_password(TEST_PASSWORD)
        user.is_active = True
        user.save()
    
    def _create_client(self):
        """
        Create a test client data to be used in testing.
        """
        try:
            ZohoClient.objects.create(**self.client_beerwulf_data)
        except Exception as e:
            print(e)
    
    def _create_profile(self):
        """
        User to create a test profile.
        """
        profile = Profile()
        profile.user = User.objects.get(pk=1)
        profile.client = ZohoClient.objects.get(pk=1)
        profile.role = 'admin'
        profile.status = 'approved'
        profile.save()

    def test_get(self):
        """
        Test the url if it will return status 301.
        """

        url = f'/billing/invoice/test-invoice-file.png/download'
        response = self.client.get(url)

        # This view will redirect user ti another URL to download the file
        # in the s3 bucket that's why we are expecting 301 status code.
        redirect_status = 301
        self.assertEqual(response.status_code, redirect_status)