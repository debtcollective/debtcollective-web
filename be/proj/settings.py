import os
import os.path
import sys
#import newrelic.agent

from url_config.django import database as db_conf
from url_config.django import cache  as cache_conf
from url_config import redis as redis_conf
from url_config.utils import delimited, apply_differences, from_env, bool_str

#newrelic.agent.initialize()

# import dev.import_debug

INTERNAL_IPS = delimited(from_env('DJANGO_INTERNAL_IPS', ''))
CANONICAL_DOMAIN = from_env('CANONICAL_DOMAIN', None)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT = lambda *args: os.path.join(PROJECT_ROOT, *args)

ENVIRONMENT = from_env('DJANGO_ENV', 'development')

IS_TEST = False

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

try:
    if sys.argv[1] in ['test', 'jenkins']:
        IS_TEST = True
except IndexError:
    pass

DEBUG = not IS_TEST and bool_str(from_env('DJANGO_DEBUG', 'false'))
TEMPLATE_DEBUG = DEBUG

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_SSL = bool_str(from_env('DJANGO_USE_SSL', ''))

ALLOWED_HOSTS = delimited(from_env('DJANGO_ALLOWED_HOSTS'))

ADMINS = [
    ('DC Errors', 'errors@debtcollective.org'),
]

MANAGERS = ADMINS


DATABASES = {
    'default': db_conf.from_url(from_env('DATABASE_URL')),
}

CONN_MAX_AGE = None

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

DJORM_POOL_OPTIONS = {
    "pool_size": 50,
    "max_overflow": 0,
    "recycle": 3600, # the default value
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

TIME_ZONE = 'UTC'
USE_TZ    = True

LANGUAGE_CODE = 'en-us'

USE_I18N = False
USE_L10N = False

DEFAULT_FILE_STORAGE = from_env('DJANGO_DEFAULT_FILE_STORAGE')

REDIS = redis_conf.from_url(from_env('REDIS_URL'))

EMAIL_BACKEND = os.environ['DJANGO_EMAIL_BACKEND']

EMAIL_HOST = from_env('DJANGO_EMAIL_HOST', None)
EMAIL_PORT = int(from_env('DJANGO_EMAIL_PORT', 0))
EMAIL_HOST_USER = from_env('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = from_env('DJANGO_EMAIL_HOST_PASSWORD')

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

#>>>>

AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = True
STATICFILES_STORAGE = from_env('DJANGO_STATICFILES_STORAGE', '') or None

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = from_env('DJANGO_STATIC_URL')

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = delimited(from_env('DJANGO_STATICFILES_FINDERS'))

SECRET_KEY = from_env('DJANGO_SECRET_KEY', strip_comments=False)

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
]

MIDDLEWARE_CLASSES = [
    'proj.middleware.CanonicalURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'proj.middleware.TimezoneMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'proj.middleware.SocialAuthErrorMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
]

EXCLUDED_MIDDLEWARES = delimited(from_env('DJANGO_INSTALLED_MIDDLEWARES_EXCEPTIONS', ''))
EXTRA_MIDDLEWARES = delimited(from_env('DJANGO_INSTALLED_MIDDLEWARES_EXTRAS', ''))

apply_differences(MIDDLEWARE_CLASSES, EXTRA_MIDDLEWARES, EXCLUDED_MIDDLEWARES)


TEMPLATE_DIRS = [
    PROJECT('templates'),
]

ROOT_URLCONF = 'proj.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'proj',

    # Third-party apps
    'django_compressor',
    'djcelery',
    'gunicorn',
    'kombu.transport.django',
    'rest_framework',
    'raven.contrib.django.raven_compat',
    'social_auth',
    'south',
    'storages',
]

EXCLUDED_APPS = delimited(from_env('DJANGO_INSTALLED_APPS_EXCEPTIONS', ''))
EXTRA_APPS = delimited(from_env('DJANGO_INSTALLED_APPS_EXTRAS', ''))

apply_differences(INSTALLED_APPS, EXTRA_APPS, EXCLUDED_APPS)

# A simple logging setup that logs to stdout/stderr. (On Heroku, that becomes the
# application's log)
if IS_TEST:
    LOG_LEVEL = 'WARNING'
else:
    LOG_LEVEL = from_env('DEBT_LOG_LEVEL')

LOG_HANDLERS = delimited(from_env('DEBT_LOG_HANDLERS'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)-8s: %(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'stream': {
            'level':LOG_LEVEL,
            'class':'logging.StreamHandler',
            'formatter': 'simple',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
        }
    },
    'loggers': {
        '': {
            'handlers': LOG_HANDLERS,
            'level': LOG_LEVEL,
            'propagate': False,
        },
        #Only log warnings and errors in the following
        'amqp': {
            'handlers' : LOG_HANDLERS,
            'level'    : 'WARNING',
            'propagate': False,
        },
        'boto': {
            'handlers' : LOG_HANDLERS,
            'level'    : 'WARNING',
            'propagate': False,
        },
        'django': {
            'handlers' : LOG_HANDLERS,
            'propagate': False,
            'level'    : 'WARNING',
        },
    }
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel'
]


# Disable South logging and test migrations
SOUTH_LOGGING_ON    = False
SOUTH_TESTS_MIGRATE = False

CACHES = {
    'default': cache_conf.from_url(from_env('DJANGO_CACHES_DEFAULT_URL')),
}

LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/signup-error/'

AUTHENTICATION_BACKENDS = [
    'social_auth.backends.facebook.FacebookBackend',
    'proj.auth.backends.EmailVerificationBackend',
    'accounts.auth.backends.PasswordResetBackend',
    'accounts.auth.backends.CaseInsensitiveModelBackend',
    'accounts.auth.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
]

EXTRA_AUTHS = delimited(from_env('DJANGO_AUTHENTICATION_BACKENDS_EXTRAS', ''))

apply_differences(AUTHENTICATION_BACKENDS, EXTRA_AUTHS, [])

AUTH_USER_MODEL = 'proj.User'

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'accounts.custom_pipelines.fetch_archived_social_auth',
    'accounts.custom_pipelines.fetch_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'accounts.custom_pipelines.get_username',
    'accounts.custom_pipelines.create_user',
    'accounts.custom_pipelines.create_archived_social_auth',
    'social_auth.backends.pipeline.social.associate_user',
    'accounts.custom_pipelines.give_gift',
    'accounts.custom_pipelines.store_social_account_data',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook',)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = USE_SSL
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/social-auth-success/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/signup-error/'
#HUH?
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'first_name', 'last_name']
SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True
SOCIAL_AUTH_SLUGIFY_USERNAMES = True
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

FACEBOOK_APP_ID         = 'FIXME'
FACEBOOK_API_SECRET     = 'FIXME'

RAVEN_CONFIG = {
    'dsn': from_env('SENTRY_DSN', 'http://publickey:privatekey@localhost/9492'),
    'public_dns': from_env('SENTRY_PUBLIC_DNS', 'http://publickey@localhost/9492'),
}

###CELERY CONFIGURATION
BROKER_URL = from_env('RABBITMQ_URL', '') or None
BROKER_POOL_LIMIT = None
BROKER_BACKEND = 'amqp'

CELERY_ALWAYS_EAGER = IS_TEST or bool_str(from_env('DJX_CELERY_ALWAYS_EAGER', 'false'))
CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
#our table is growing too fast and times out. so let's try cleaning up tasks in a shorter interval.
CELERY_TASK_RESULT_EXPIRES=1*60*60*4

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'core-cleanup': {
        'task': 'core.tasks.cleanup',
        'schedule': crontab(hour=5, minute=0)
    }
}

USE_LOCKDOWN = bool_str( from_env('USE_LOCKDOWN', 'False') )
LOCKDOWN_PASSWORDS = (from_env('LOCKDOWN_PASSWORD', None),)

ROOT_URLCONF = 'proj.urls'

WSGI_APPLICATION = 'proj.wsgi.application'
