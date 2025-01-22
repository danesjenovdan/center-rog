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

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    'RESULTS_CACHE_SIZE': 500,
}

try:
    from .local import *
except ImportError:
    pass


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_EMAIL = 'dummy@email.com'


def request_filter(record):
    if isinstance(record.args[0], str):
        if record.args[0] == "Not Found":
            return False
        if record.args[0].startswith("GET /media/"):
            return False
        if record.args[0].startswith("GET /static/"):
            return False
    return True

DEFAULT_LOGGING["filters"]["request_filter"] = {
    "()": "django.utils.log.CallbackFilter",
    "callback": request_filter,
}
DEFAULT_LOGGING["handlers"]["console"]["filters"] = ["request_filter"]
DEFAULT_LOGGING["handlers"]["django.server"]["filters"] = ["request_filter"]
