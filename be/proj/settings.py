"""
Django settings for proj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
"""

# Build paths inside the project
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

from envconfig import get_envconfig
get_envconfig(globals())

# Override the above with environment keys generated on the production server

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proj',
    'proj.gather',
    'south'
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'proj.urls'
# XXX: unsure why 'be' needs to be left out of the initial path (karissa)
WSGI_APPLICATION = 'proj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'debtis',
        'USER': 'debtis',
        'PASSWORD': 'debtis',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Parse database configuration from $DATABASE_URL
import dj_database_url
config = dj_database_url.config()
if config:
    DATABASES['default'] = config

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = [
  '.debtcollective.org',
  '.debt-is.herokuapp.com',
  '.debt-is-staging.herokuapp.com',
  'localhost'
]

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.environ.get('STATIC_ROOT', 'staticfiles')
STATIC_URL = '/static/'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\','/'),
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Misc.
AUTH_PROFILE_MODULE = 'gather.UserProfile'
MAP_PASSWORD = os.environ.get('MAP_PASSWORD', '')
STRIPE_KEY= os.environ.get('STRIPE_KEY','')