"""
Django settings for i_gng project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP #allauth < 1.8
from django.core.urlresolvers import reverse_lazy


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zn($ym#*&)7t9mtfd6yxw_rme5x(&c-*@1t)_da3sf%!^1s%)c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'debug_toolbar',


    # the most necessary tool of all
    'rest_framework',
    'rest_framework.authtoken',
    'drf_openapi',

    # some niceties for forms
    # 'materializecssform',
    'crispy_forms',
    'crispy_forms_materialize',

    # dat shell_plus && UUIDfield
    'django_extensions',

    # for mangling images
    'imagekit',

    # for tagging
    'taggit',
    'taggit_autosuggest',
    'taggit_serializer',

    # for logging
    'raven.contrib.django.raven_compat',

    # for auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',

    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.flickr',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.twitter',

    # our apps
    'common',
    'images',
    'lapses',
    'token_mgmt',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'i_gng.urls'

WSGI_APPLICATION = 'i_gng.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR + "/media/"


TEMPLATE_DIRS = (
    BASE_DIR + "/tmpl",
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
)
## Template Tags for AllAUth

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tmpl'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_URL = reverse_lazy('account_login')
LOGIN_REDIRECT_URL = '/i/i/'

SITE_ID = 1
SITE_URL = "https://i.gng.io"

# other configs

CRISPY_TEMPLATE_PACK = 'materialize_css_forms'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'bootstrap4', 'materialize_css_forms')
# IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_as_path'
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'images.namers.igng_source_name_as_path'

SOCIALACCOUNT_PROVIDERS = {
    'persona':
         {'AUDIENCE': 'http://i.gng.io',
          'REQUEST_PARAMETERS': {'siteName': 'iGNG'}
         }
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
}
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER":"common.serializers.UserDetailsSerializer"
}

# CELERY
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

try:
    path = os.path.join(BASE_DIR, "i_gng", "local_settings.py")
    f = open(path)
    exec(f.read())
except IOError:
    print("No local settings found!")