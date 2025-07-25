"""
Django settings for rog project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from django.utils.log import DEFAULT_LOGGING
from wagtail.embeds.oembed_providers import all_providers

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Log to console even when debug is off
DEFAULT_LOGGING["handlers"]["console"]["filters"] = []

# Application definition

INSTALLED_APPS = [
    "wagtail_modeltranslation",
    "wagtail_modeltranslation.makemigrations",
    "wagtail_modeltranslation.migrate",
    "wagtail_modeladmin",
    "home",
    "search",
    "users",
    "events",
    "news",
    "payments",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "jsonify",
    "wagtailmedia",
    "wkhtmltopdf",
    "wagtailautocomplete",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "wagtail_rangefilter",
    "rangefilter",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "rog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "rog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST', 'db'),
        'NAME': os.getenv('DB_NAME', 'wagtail'),
        'USER': os.getenv('DB_USERNAME', 'wagtail'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'changeme'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "sl"

TIME_ZONE = "Europe/Ljubljana"

USE_I18N = True
WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_TZ = True

# possible values of the language_code field
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('sl', "Slovenian"),
    ('en', "English"),
]

# User settings
AUTH_USER_MODEL = 'users.User'
WAGTAIL_USER_EDIT_FORM = 'users.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'users.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = [
    "prima_id",
    "email_confirmed",
    "allow_marketing",
    "address_1",
    "address_2",
    "legal_person_receipt",
    "legal_person_name",
    "legal_person_address_1",
    "legal_person_address_2",
    "legal_person_tax_number",
    "legal_person_vat",
    "public_profile",
    "public_username",
    "description",
    "link_1",
    "link_2",
    "link_3",
    "contact",
    "workshops_attended",
    "interests",
    "birth_date",
    "gender",
    "gender_other",
    "gallery",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, '../locale'),
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LOGIN_REDIRECT_URL = "/profil/"
LOGIN_URL = "/prijava/"
LOGOUT_REDIRECT_URL = "/"

# Wagtail settings

WAGTAIL_SITE_NAME = "rog"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAILMODELTRANSLATION_TRANSLATE_SLUGS = True

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"

WAGTAIL_ALLOW_UNICODE_SLUGS = False

WAGTAILIMAGES_IMAGE_MODEL = "home.CustomImage"

WAGTAILMEDIA = {
    "AUDIO_EXTENSIONS": [],
    "VIDEO_EXTENSIONS": ["mp4", "webm"],
}


# Add extra embed providers
datawrapper = {
    "endpoint": "https://api.datawrapper.de/v3/oembed",
    "urls": [
        r'^https?://datawrapper.dwcdn.net/.+$',
        r'^https?://www.datawrapper.de/.+$',
    ],
}

jotform = {
    "endpoint": "https://www.jotform.com/oembed",
    "urls": [
        r'^https?://form.jotform.com/.+$',
        r'^https?://www.jotform.com/.+$',
    ],
}

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "rog.embeds.canonical_oembed",
        "providers": [jotform],
    },
    {
        "class": "wagtail.embeds.finders.oembed",
        "providers": [*all_providers, datawrapper, jotform],
    },
]

WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': False,
    'enable-local-file-access': True,
    'disable-smart-shrinking': True,
    'print-media-type': True,
    'page-size': 'A4',
    'margin-top': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'margin-right': '0',
}

WKHTMLTOPDF_CMD = 'xvfb-run -a wkhtmltopdf'

# Prima settings
PRIMA_API_KEY = os.getenv('PRIMA_API_KEY', 'example')
PRIMA_URL = "https://centerrog.primacloud.si/bin/sysfcgi.fx"

# Custom
COLOR_SCHEMES = [
    ("brown", "Rjava"),
    ("light-gray", "Svetlo siva"),
    ("dark-gray", "Temno siva"),
    ("light-blue", "Svetlo modra"),
    ("dark-blue", "Temno modra"),
    ("light-green", "Svetlo zelena"),
    ("dark-green", "Temno zelena"),
    ("dark-purple", "Temno vijolična"),
    ("light-purple", "Svetlo vijolična"),
    ("red", "Rdeča"),
    ("beige", "Bež"),
    ("beige-gray", "Umazana siva"),
    ("orange", "Oranžna"),
    ("pink", "Roza"),
    ("yellow", "Rumena"),
    ("white", "Bela"),
]

# Payments
PAYMENT_IDS = os.getenv('PAYMENT_IDS', '123')
PAYMENT_BASE_URL = os.getenv('PAYMENT_BASE_URL', 'https://testeplacila.si/vstop/index')
REGISTRATION_NUMBER = os.getenv('REGISTRATION_NUMBER', '0000000')
PANTHEON_URL = os.getenv('PANTHEON_URL', '')

# CORS
ALLOWED_HOSTS = ['localhost', 'rog.lb.djnd.si']
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", 'https://rog.lb.djnd.si']
CORS_ALLOWED_ORIGINS = ["http://localhost:8000", 'https://rog.lb.djnd.si']


AUTHENTICATION_BACKENDS = ['users.backends.CaseInsensitiveModelBackend']
