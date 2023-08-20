from django.shortcuts import _get_queryset


def get_object_or_None(model, *args, **kwargs):
    """
    A shortcut function for querying that returns None if an object
    does not exist instead of raising an error.
    """

    queryset = _get_queryset(model)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
