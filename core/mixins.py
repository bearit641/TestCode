import math


class RequireModelMixin:
    """
    An interface that requires a class to
    have a model attribute.
    """

    def _get_model(self, *args, **kwargs):
        """
        A private method that fetches the
        applied model attribute.
        """
        try:
            return getattr(self, 'model')
        except AttributeError:
            raise NotImplementedError(
                f'{self.__class__.__name__} implements the '
                f'RequireModelMixin but no model attribute is '
                f'declared.'
            )

    def get_queryset(self, *args, **kwargs):
        """
        A virtual method that returns all
        values from a model by default.
        """
        Model = self._get_model(*args, **kwargs)
        return Model.objects.all()


class PaginationMixin:
    """
    An interface that allows a class
    to implement a pagination attribute.
    """

    def _get_pagination(self, *args, **kwargs):
        """
        A private method that fetches the
        applied pagination attribute.
        """
        try:
            pagination = getattr(self, 'pagination')
        except AttributeError:
            raise NotImplementedError(
                f'{self.__class__.__name__} implements the '
                f'RequireModelMixin but no pagination attribute '
                f'is declared.'
            )
        try:
            assert isinstance(pagination, int)
        except AssertionError:
            raise ValueError(
                'pagination attribute must be an integer.'
            )
        return pagination

    def get_indices_for_page(self, page, *args, **kwargs):
        """
        Accepts a page number, then returns the index range
        for that page based on the pagination as a tuple.

            :param page: :type int:
                - The page number.
        """
        page = int(page)
        try:
            assert page >= 1
        except AssertionError:
            raise ValueError(
                f'`page` should not be less than 1. '
                f'Page received: {page}'
            )
        # Offset page by 1 for algorithmic purposes.
        page -= 1
        pagination = self._get_pagination(*args, **kwargs)
        start = page * pagination
        end = start + pagination
        return start, end


class PageCountMixin(PaginationMixin, RequireModelMixin):
    """
    A mixin interface that provides a method that
    calculates the amount of pages possible for
    a queryset provided by the `RequireModelMixin`.
    """

    def get_page_count(self, *args, **kwargs):
        """
        Returns the maximum amount of pages possible
        for a queryset based on the configurations
        inherited from `PaginationMixin`.
        """
        pagination = self._get_pagination(*args, **kwargs)
        queryset_count = self.get_queryset(*args, **kwargs).count()
        try:
            return math.ceil(queryset_count / pagination)
        except ValueError:
            return 0
        except ZeroDivisionError:
            return 0

    def get_page_range(self, offset=1, *args, **kwargs):
        """
        Returns the possible pages as a range.

            :param offset: :type int:
                - This offsets the numerical value of the first
                    and last page. Defaults as 1.
        """
        return range(offset, self.get_page_count(*args, **kwargs) + offset)

    def get_page_list(self, offset=1, *args, **kwargs):
        """
        Returns all the possible pages as a list.

            :param offset: :type int:
                - This offsets the numerical value of the first
                    and last page. Defaults as 1.
        """
        return [i for i in self.get_page_range(offset=offset)]
