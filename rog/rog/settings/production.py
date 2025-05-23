from .base import *
import sentry_sdk

DEBUG = bool(os.getenv('DJANGO_DEBUG', False))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DATABASE_NAME', 'wagtail'),
        'USER': os.getenv('DJANGO_DATABASE_USERNAME', 'wagtail'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD', 'changeme'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST', 'db'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', '5432'),
    }
}

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'thisshouldbesecret')

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = os.getenv('BASE_URLS', 'https://center-rog.si').split(',')

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = CSRF_TRUSTED_ORIGINS[0]

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', '/static/')
STATIC_URL = os.getenv('DJANGO_STATIC_URL_BASE', '/static/')

# S3 Storage
if os.getenv('DJANGO_ENABLE_S3', False):
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    }
    AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID', '<TODO>')
    AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY', '<TODO>')
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME', 'djnd')
    AWS_DEFAULT_ACL = 'public-read' # if files are not public they won't show up for end users
    AWS_QUERYSTRING_AUTH = False # query strings expire and don't play nice with the cache
    AWS_LOCATION = os.getenv('DJANGO_AWS_LOCATION', 'rog')
    AWS_S3_REGION_NAME = os.getenv('DJANGO_AWS_REGION_NAME', 'fr-par')
    AWS_S3_ENDPOINT_URL = os.getenv('DJANGO_AWS_S3_ENDPOINT_URL', 'https://s3.fr-par.scw.cloud')
    AWS_S3_SIGNATURE_VERSION = os.getenv('DJANGO_AWS_S3_SIGNATURE_VERSION', 's3v4')
    AWS_S3_FILE_OVERWRITE = False # don't overwrite files if uploaded with same file name

try:
    from .local import *
except ImportError:
    pass


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', '')
EMAIL_HOST_USER = os.getenv('EMAIL_USERNAME', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_USE_TLS = bool(os.getenv('EMAIL_USE_TLS', ''))
EMAIL_USE_SSL = bool(os.getenv('EMAIL_USE_SSL', ''))
FROM_EMAIL = os.getenv('FROM_EMAIL', 'dummy@email.com')
DEFAULT_FROM_EMAIL = FROM_EMAIL



SENTRY_DSN = os.getenv('SENTRY_DSN', '')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', 0.001)),
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', 0.001)),
    )
