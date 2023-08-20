import json
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load secrets
try:
    print(BASE_DIR)
    with open(BASE_DIR / 'keys.json', 'r') as fh:
        keys = json.loads(fh.read())
        fh.close()
except FileNotFoundError:
    msg = 'Configure keys.json in the settings folder'
    raise ImproperlyConfigured(msg)
except ValueError as err:
    raise err


def get_key(key, keys=keys, optional=False):
    """
    Retrieve a configuration key value from a key dictionary
    - param key: Settings config dictionary key
    - type key: str
    - param keys: Key dictionary.
        Default: Values from keys.json as dictionary
    - type keys: dict
    - param optional: A boolean value that defines if the value is optional
        Default: False
    returns: Value from a key dictionary
    """
    try:
        return keys[key]
    except KeyError:
        if not optional:
            raise ImproperlyConfigured(
                f'Set the "{key}" setting in keys.json '
                'or the keys dictionary you provided'
            )


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_key('SECRET_KEY')

# 3rd party API Integrations
ROYAL_MAIL_USERNAME = get_key('ROYAL_MAIL_USERNAME')
ROYAL_MAIL_PASSWORD = get_key('ROYAL_MAIL_PASSWORD')
YODEL_CLIENT_ID = get_key('YODEL_CLIENT_ID')
YODEL_TRACKING_SECRET = get_key('YODEL_TRACKING_SECRET')
HERMES_AUTH_BASE_PATH = get_key('HERMES_AUTH_BASE_PATH')
HERMES_CLIENT_ID = get_key('HERMES_CLIENT_ID')
HERMES_CLIENT_SECRET = get_key('HERMES_CLIENT_SECRET')
HERMES_TRACKING_BASE_PATH = get_key('HERMES_TRACKING_BASE_PATH')
HERMES_API_KEY = get_key('HERMES_API_KEY')
LANDMARK_API_TRACKING_URL = get_key('LANDMARK_API_TRACKING_URL')
LANDMARK_API_USERNAME = get_key('LANDMARK_API_USERNAME')
LANDMARK_API_PASSWORD = get_key('LANDMARK_API_PASSWORD')

# Hubecloud API Integrations
SIGNUP_ENDPOINT = get_key('SIGNUP_ENDPOINT')
SIGNUP_API_KEY = get_key('SIGNUP_API_KEY')
APPROVAL_ENDPOINT = get_key('APPROVAL_ENDPOINT')
APPROVAL_API_KEY = get_key('APPROVAL_API_KEY')
PASSWORD_RESET_ENDPOINT = get_key('PASSWORD_RESET_ENDPOINT')
PASSWORD_RESET_API_KEY = get_key('PASSWORD_RESET_API_KEY')
SEND_INVOICE_ENDPOINT = get_key('SEND_INVOICE_ENDPOINT')
SEND_INVOICE_API_KEY = get_key('SEND_INVOICE_API_KEY')

# API enablement
DISABLE_COURIER_ROYALMAIL = bool(
    get_key('DISABLE_COURIER_ROYALMAIL', optional=True)
) or False
DISABLE_COURIER_YODEL = bool(
    get_key('DISABLE_COURIER_YODEL', optional=True)
) or False
DISABLE_COURIER_HERMES = bool(
    get_key('DISABLE_COURIER_HERMES', optional=True)
) or False
DISABLE_COURIER_SECUREDMAIL = bool(
    get_key('DISABLE_COURIER_SECUREDMAIL', optional=True)
) or False
DISABLE_COURIER_LANDMARK = bool(
    get_key('DISABLE_COURIER_LANDMARK', optional=True)
) or False

# Configurtions:

# A local configuration where if this is True,
# all test data are excluded from all queries
# for the despatch cloud record model.
EXCLUDE_DC_TEST_DATA = True

# SECURITY WARNING: don't run with debug turned on in production!
environment = get_key('ENVIRONMENT')
DEBUG = True if environment == 'staging' else False
#DEBUG = True

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'charts',
    'clients',
    'despatch_cloud',
    'hubcommon',
    'invoicing',
    'gardening_direct',
    'mobile_integrations',
    'parcel_costs',
    'parcel_subscriptions',
    'providers',
    'revenue',
    'scanner',
    'services',
    'signup',
    'surcharges',
    'tracking',
    'unbilled_parcel',
    'users',
    'washing_machine_api',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_PARTY_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware'
]

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'hubeurope.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hubeurope.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_key('DB_NAME'),
        'USER': get_key('DB_USER'),
        'PASSWORD': get_key('DB_PASSWORD'),
        'HOST': get_key('DB_HOST'),
        'PORT': ''
        # 'NAME': 'hubeurope',
        # 'USER': '<RDS_USER>', # Note: Ideally not ROOT for better security
        # 'PASSWORD': '<RDS_PW>',
        # 'HOST': '<RDS_HOST>',
        # 'PORT': '',
     }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Default permissions and authentications
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.LimitOffsetPagination'
    ),
    'PAGE_SIZE': 100
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Jersey'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'https://hubeurope-new-static-files.s3-eu-west-1.amazonaws.com/static/'
STATIC_ROOT = BASE_DIR / 'assets'
STATICFILES_DIRS = [
    (BASE_DIR / 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

LOGIN_REDIRECT_URL = 'front_page'
LOGOUT_REDIRECT_URL = 'login'

# Couriers
COURIERS = ['', 'Hermes', 'Yodel', 'Royal Mail']

# AWS Configuration Keys
AWS_ACCESS_KEY_ID = get_key('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_key('AWS_SECRET_ACCESS_KEY')

# AWS S3 Bucket Configuration
AWS_BUCKETS = {
    'BILLING_FILE_BUCKET_NAME': get_key('BILLING_FILE_BUCKET_NAME'),
    'TRACKING_INPUT_BUCKET_NAME': get_key('TRACKING_INPUT_BUCKET_NAME'),
    'TRACKING_OUTPUT_BUCKET_NAME': get_key('TRACKING_OUTPUT_BUCKET_NAME'),
    'INVOICE_BUCKET_NAME': get_key('INVOICE_BUCKET_NAME'),
    'RATES_UPDATE_BUCKET_NAME': get_key('RATES_UPDATE_BUCKET_NAME'),
    'EXPRESS_FILE_BUCKET_NAME': get_key('EXPRESS_FILE_BUCKET_NAME'),
}

# AWS Parameter Store Configuration
AWS_PARAMETER = {}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

REDIS_HOST = get_key('REDIS_HOST')
REDIS_PORT = get_key('REDIS_PORT')
REDIS_PASSWORD = get_key('REDIS_PASSWORD')
REDIS_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "PASSWORD": REDIS_PASSWORD,
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "hubeurope"
    }
}
