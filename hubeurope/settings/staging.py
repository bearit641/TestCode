import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# Update when staging domain is defined
ALLOWED_HOSTS = (
    (get_key('ALLOWED_HOSTS', optional=True) or '').split(',')
    or ['staging.hubeurope.com']
)

DEBUG = False

SENTRY_DSN = get_key('SENTRY_DSN', optional=True)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
