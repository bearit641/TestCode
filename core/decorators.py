class CacheStatus:
    """
    A class that serves as an enum for
    caching statuses.
    """

    INVALID = 1
    UNKNOWN = 2
    VALID = 3


class CachedMethod:
    """
    A wrapper class for methods that implements
    application-scoped caching strategies for
    values that take a while to retrieve.
    """

    def __init__(self, method, *args, **kwargs):
        self._method = method
        self._cache_status = CacheStatus.UNKNOWN
        self._cached_value = None

    @property
    def cached(self):
        """
        Returns the cached value.
        """
        return self._cached_value

    @property
    def status(self):
        """
        Returns the status of the cached value.
        """
        return self._cache_status

    def invalidate(self):
        """
        Invalidates the cache.
        """
        self._cache_status = CacheStatus.INVALID

    def validate(self):
        """
        Validates the cache.
        """
        self._cache_status = CacheStatus.VALID

    def _run_method(self, context=None, *args, **kwargs):
        """
        Returns the result of the given method.
        """
        if context:
            return self._method(context, *args, **kwargs)
        return self._method(*args, **kwargs)

    def retrieve_value(self, context=None, *args, **kwargs):
        """
        Retrieves the return result of the given
        method if the cache is less than valid, else
        the value from the cache is used.

        If the value is successfully retrieved, then
        the cache will be validated automatically soon
        after.
        """
        if self.status < CacheStatus.VALID:
            try:
                value = self._run_method(context=context, *args, **kwargs)
            except Exception as e:
                raise Exception(
                    f'Exception occurred: {e}. Cannot validate cache.'
                )
            self.validate()
            self._cached_value = value
            return value
        return self._cached_value

    def get_wrapper(self, *args, **kwargs):
        """
        Returns a wrapper method with reference to
        the method's cache.
        """
        def wrapper(context, *args, **kwargs):
            return self.retrieve_value(context=context, *args, **kwargs)
        wrapper.invalidate = self.invalidate
        wrapper.get_cached = lambda: self.cached
        wrapper.__cache__ = self
        return wrapper

    def __call__(self, context=None, *args, **kwargs):
        return self.retrieve_value(context=context, *args, **kwargs)


def cached_method(callback):
    """
    A decorator that caches the return value of a function in memory
    by assigning the value as a new attribute of the current class.
    This utilizes the CachedMethod class into the method to add properties.
    """
    return CachedMethod(callback).get_wrapper()
