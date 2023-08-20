import csv
from io import BytesIO

from django.http import HttpResponse


class CSVReport:
    """
    A template class for containing logic for
    rendering values into a CSV file.
    """

    headers = []
    row_data = []
    footer_data = []
    filename = 'report'

    content_type = 'text/csv'

    def build_csv(self, writer, *args, **kwargs):
        """
        Render all configurured values into a csv writer.
        """
        writer = self.build_headers(writer, *args, **kwargs)
        writer = self.build_content(writer, *args, **kwargs)
        writer = self.build_footer(writer, *args, **kwargs)
        return writer

    @property
    def response(self):
        """
        Returns the csv file as an HttpResponse.
        """
        filename = self.get_filename()
        response = HttpResponse(content_type=self.get_content_type())
        response['Content-Disposition'] = (
            f'attachment; filename="{filename}.csv"')
        writer = csv.writer(response)
        writer = self.build_csv(writer)
        return response

    @property
    def output(self):
        """
        Returns a BytesIO object containing the report.
        """
        _output = BytesIO()
        writer = csv.writer(_output)
        writer = self.build_csv(writer)
        return _output

    def attach_to_email(self, message):
        """
        Attaches the report into an email object.

        - Parameters:

            message: A Django EmailMultiAlternatives object.
        """
        filename = self.get_filename()
        message.attach(
            f'{filename}.csv',
            self.output.getvalue(),
            self.get_content_type()
        )

    def get_filename(self, *args, **kwargs):
        """
        Returns the filename of the report.
        """
        return self.filename

    def get_content_type(self, *args, **kwargs):
        """
        Returns the content type to be used for outputs.
        """
        return self.content_type

    def get_headers(self, *args, **kwargs):
        """
        A virtual method for setting up headers.
        """
        return self.headers

    def get_row_data(self, *args, **kwargs):
        """
        A virtual method for setting up data per row.
        """
        return self.row_data

    def get_footer_data(self, *args, **kwargs):
        """
        A virtual method for setting up data for the footer.
        """
        return self.footer_data

    def build_headers(self, writer, *args, **kwargs):
        """
        A virtual method for rendering headers.
        """
        headers = self.get_headers(*args, **kwargs)
        writer.writerow(headers)
        return writer

    def build_content(self, writer, *args, **kwargs):
        """
        A virtual method for rendering data.
        """
        row_data = self.get_row_data(*args, **kwargs)
        for row_datum in row_data:
            writer.writerow(row_datum)
        return writer

    def build_footer(self, writer, *args, **kwargs):
        """
        A virtual method for rendering headers.
        """
        footer_data = self.get_footer_data(*args, **kwargs)
        writer.writerow(footer_data)
        return writer
