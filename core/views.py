import json

from braces.views import JSONResponseMixin

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import View

from .mixins import PageCountMixin
from .mixins import PaginationMixin
from .mixins import RequireModelMixin
from .reports import CSVReport


class JSONView(JSONResponseMixin, TemplateView):
    """
    A view dedicated for responding customized json data.

    Reference:
    https://docs.djangoproject.com/en/3.0/topics/class-based-views/mixins/#more-than-just-html
    """

    disable_get = False

    def render_to_response(self, context, **response_kwargs):
        """
        This totally overrides the template view's render_to_response
        method. Rather than responding an html rendered through django
        templates, this will response a json that contains the values
        returned by get_context_data.
        """
        return self.render_json_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        if self.disable_get:
            raise Http404(f'GET is disabled for {self.__class__.__name__}')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Do the same thing with Post.
        """
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SchemaJSONView(PaginationMixin, RequireModelMixin, JSONView):
    """
    A JSON view that provides a front end interface
    for fetching values on demand from a model.

    Works similar with GraphQL implementations, but is
    strictly readonly.

    - Query param overrides:

        query - A list of database column names to query.
        ids - Specific primary keys of values that
            will be fetched. Only works if `by_id`
            is True.
        pagination - Overrides the pagination of
            the values. Only applicable if `paginate`
            is True.
        page - Defines the page number. Only
            applicable if `paginate` is True.
    """

    # Paginate values if True
    paginate = False

    # The amount of values for each page.
    pagination = 10

    # Configure the SchemaJSONView to accept specific ids.
    by_id = False

    # Configure query to be able to access properties.
    # If set to False, a more optimal database query
    # will be used at the expense of access to model
    # properties. Can be overriden through query
    # params as well.
    access_properties = False

    def add_custom_values(self, query_value, *args, **kwargs):
        """
        A virtual method for overriding the values
        of each query result before being sent as
        a response.
        """
        return query_value

    def get_params(self, *args, **kwargs):
        """
        Returns the parsed body params.
        """
        return json.loads(self.request.body)

    def get_ordering(self, *args, **kwargs):
        """
        Returns the parameters for ordering/sorting
        the queryset.
        """
        params = self.get_params(*args, **kwargs)
        order = params.get('order', 'ascending')
        order_by = params.get('order_by', [])
        if order == 'descending':
            order_by = [str(f'-{value}') for value in order_by]
        return order_by

    def get_context_data(self, *args, **kwargs):
        params = self.get_params(*args, **kwargs)
        access_properties = (
            json.loads(params.get('access_properties', 'false')) is True
            or self.access_properties
        )
        ordering = self.get_ordering(*args, **kwargs)

        ids = params.get('ids') or []
        if self.by_id:
            if not ids:
                return {'data': {}}

        query = params.get('query') or []
        queryset = self.get_queryset(*args, **kwargs)
        if self.by_id:
            queryset = queryset.filter(pk__in=ids)

        queryset = queryset.order_by(*ordering)
        if self.paginate:
            pagination = (
                params.get('pagination')
                or self._get_pagination(*args, **kwargs)
            )
            page = params.get('page') or 1
            start, end = self.get_indices_for_page(page, *args, **kwargs)
            queryset = queryset[start:end]

        if not access_properties:
            values = queryset.only(*query).values(*query)
        else:
            values = []
            for value in queryset:
                attr_values = {}
                for attr in query:
                    attr_values[attr] = getattr(value, attr, None)
                values.append(attr_values)

        raw_data = list(values)
        data = []
        for query_value in raw_data:
            data.append(self.add_custom_values(query_value, *args, **kwargs))
        return {'data': data}


class SchemaTableJSONView(PageCountMixin, SchemaJSONView):
    """
    A custom preset view dedicated for sending responses
    to SchemaFetchers from the front-end.
    """

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_count'] = self.get_page_count()
        context['pages'] = self.get_page_list()
        context['count'] = self.get_queryset().count()
        return context


class CSVReportView(View):
    """
    View for responding csv files built using the CSVReport class.
    """

    report_class = CSVReport

    def get_report_args(self, *args, **kwargs):
        """
        Overridable to setup custom args for the report class.
        """
        return args

    def get_report_kwargs(self, *args, **kwargs):
        """
        Overridable to setup custom kwargs for the report class.
        """
        return kwargs

    def _get_report_class(self, *args, **kwargs):
        """
        Validates then returns the report class.
        """
        # Validate report class
        error_message = (
            '`report_class` received an invalid value. Please '
            'insert a class that extends `CSVReport`'
        )
        try:
            assert issubclass(self.report_class, CSVReport)
        except AssertionError:
            raise NotImplementedError(error_message)
        except TypeError:
            raise TypeError(error_message)
        return self.report_class

    def setup_report(self, *args, **kwargs):
        """
        Sets up the report.
        """
        report_args = self.get_report_args(*args, **kwargs)
        report_kwargs = self.get_report_kwargs(*args, **kwargs)
        report_class = self._get_report_class(*args, **kwargs)
        report = report_class(*report_args, **report_kwargs)
        self.report = report
        return report

    def get_response(self, *args, **kwargs):
        """
        Returns the output of the response property of the report.
        """
        return self.setup_report(*args, **kwargs).response

    def get(self, request, *args, **kwargs):
        return self.get_response(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get_response(*args, **kwargs)


class SoftDeleteView(LoginRequiredMixin, DeleteView):
    """
    Custom view for deleting an object which instead of
    calling the `delete` object method, just calls `soft_delete`.
    This strictly enforces that at the very least, authenticated
    users are the only ones with the ability to delete.

    Make sure that the model used extends BaseModel.
    """

    success_message = '{} successfully removed.'

    def get_success_message(self):
        """
        Return message to be displayed after successful deletion.
        """
        return self.success_message.format(self.object)

    def delete(self, request, *args, **kwargs):
        """
        Call the soft_delete() method on the fetched object and
        then redirect to the success URL.
        """
        self.object = self.get_object()
        self.object.soft_delete(user=self.request.user)

        # create success message
        success_message = self.get_success_message()
        messages.success(self.request, success_message)

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
