from django import forms

from core.logs_handler import logger


class BillingFileForm(forms.Form):
    """
    Form for uploading Billing Files.
    """

    billing_file = forms.FileField(label='Excel or CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('billing_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            # Check if the file is supported. We only want .csv, .xlsb and
            # .xlsx

            valid_extensions = ['csv', 'xlsb', 'xlsx']
            if extension not in valid_extensions:
                raise forms.ValidationError(
                    'File is not supported. Please use csv, xlsb or xlsx.'
                )
        return cleaned_data


class SurchargeRatesForm(forms.Form):

    """
    Form for Surcharge Rates File.
    """

    surcharge_rate_file = forms.FileField(label='CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('surcharge_rate_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            valid_extensions = ['csv']

            # Check if the file is supported. We only want .csv extension.
            if extension in valid_extensions:
                return cleaned_data
            else:
                logger.info('File is not supported. Please upload a csv file only.')
                raise forms.ValidationError(
                    'File is not supported. Please upload a csv file only.'
                )


class ServiceForm(forms.Form):

    """
    Form for Service File.
    """

    service_file = forms.FileField(label='CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('service_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            valid_extensions = ['csv']

            # Check if the file is supported. We only want .csv extension.
            if extension in valid_extensions:
                return cleaned_data
            else:
                logger.info('File is not supported. Please upload a csv file only.')
                raise forms.ValidationError(
                    'File is not supported. Please upload a csv file only.'
                )


class ZoneForm(forms.Form):

    """
    Form for Service File.
    """

    zone_file = forms.FileField(label='CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('zone_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            valid_extensions = ['csv']

            # Check if the file is supported. We only want .csv extension.
            if extension in valid_extensions:
                return cleaned_data
            else:
                logger.info('File is not supported. Please upload a csv file only.')
                raise forms.ValidationError(
                    'File is not supported. Please upload a csv file only.'
                )


class WeightClassForm(forms.Form):

    """
    Form for Service File.
    """

    weight_class_file = forms.FileField(label='CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('weight_class_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            valid_extensions = ['csv']

            # Check if the file is supported. We only want .csv extension.
            if extension in valid_extensions:
                return cleaned_data
            else:
                logger.info('File is not supported. Please upload a csv file only.')
                raise forms.ValidationError(
                    'File is not supported. Please upload a csv file only.'
                )


class SalesForm(forms.Form):

    """
    Form for Service File.
    """

    sales_file = forms.FileField(label='CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('sales_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            valid_extensions = ['csv']

            # Check if the file is supported. We only want .csv extension.
            if extension in valid_extensions:
                return cleaned_data
            else:
                logger.info('File is not supported. Please upload a csv file only.')
                raise forms.ValidationError(
                    'File is not supported. Please upload a csv file only.'
                )


class CostForm(forms.Form):

    """
    Form for Service File.
    """

    cost_file = forms.FileField(label='CSV File')

    def clean(self):
        cleaned_data = super().clean()
        filename = self.cleaned_data.get('cost_file')
        if filename:
            filename = filename.name
            parted_filename = filename.rpartition('.')
            extension = parted_filename[2]

            valid_extensions = ['csv']

            # Check if the file is supported. We only want .csv extension.
            if extension in valid_extensions:
                return cleaned_data
            else:
                logger.info('File is not supported. Please upload a csv file only.')
                raise forms.ValidationError(
                    'File is not supported. Please upload a csv file only.'
                )
