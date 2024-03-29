from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ig!t8bbw1tz&4wl2oqwbrw5b@p@(!y@l$ym46+#xt+q7k%$#3w"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = 'http://localhost:8000'

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_EMAIL = 'dummy@email.com'
