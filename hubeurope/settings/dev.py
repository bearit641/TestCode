from .base import *


ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = True

INSTALLED_APPS += [
    'django_extensions',
]

STATIC_URL = '/static/'
