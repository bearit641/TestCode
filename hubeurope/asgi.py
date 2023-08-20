"""
ASGI config for hubeurope project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

env = os.getenv('ENVIRONMENT', 'prod')
# Auto evaluate similar environment names
if env in ('production', 'live'):
    env = 'prod'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'hubeurope.settings.{env}')

application = get_asgi_application()
