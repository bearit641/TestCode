"""
Template tags for handling front-end navigation interfaces.
"""
from django import template
from django.urls import resolve


register = template.Library()


def current_url_equals(context, url_name, menu=False, **kwargs):
    """
    A utility method for evaluating that a certain
    reverse url matches the current page.
    """
    resolved_url = None
    url_string = ''
    try:
        resolved_url = resolve(context.get('request').path)
    except AttributeError:
        pass
    except ValueError:
        pass
    namespace = getattr(resolved_url, 'namespace', None)
    if menu:
        return namespace == url_name
    resolved_url_name = getattr(resolved_url, 'url_name', None)
    url_prefix = f'{namespace}:' if namespace else ''
    url_string = (
        f'{url_prefix}{resolved_url_name}'
        if resolved_url is not None else ''
    )
    matches = resolved_url is not None and url_name == url_string
    if matches and kwargs:
        for key in kwargs:
            kwarg = kwargs.get(key)
            resolved_kwarg = resolved_url.kwargs.get(key)
            if not resolved_kwarg or kwarg != resolved_kwarg:
                return False
    return matches


@register.simple_tag(takes_context=True)
def current(context, url_name, return_value='active', **kwargs):
    """
    Template tag for evaluating if the current page matches
    a given reverse url reference.
    """
    matches = current_url_equals(context, url_name, **kwargs)
    return return_value if matches else ''


@register.simple_tag(takes_context=True)
def current_menu(context, url_name, return_value='show', **kwargs):
    """
    Template tag for evaluating if the current page is
    under a certain sub menu in the navigation bar.
    """
    matches = current_url_equals(context, url_name, menu=True, **kwargs)
    return return_value if matches else ''
