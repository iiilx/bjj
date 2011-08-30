

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


AUTH_PROFILE_MODULE = 'app.UserProfile'

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1 

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

import os

PROJECT_DIR = os.getcwd()

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sentry.client.middleware.Sentry404CatchMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "socialauth.context_processors.facebook_api_key",
    "app.processors.categories",
    "app.processors.fbook_url",
    "app.processors.top_polls_processor",
    "app.processors.most_discussed_processor",
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'bjj.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', #this is for db sessions
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.comments',
    'bjj.app',
    'bjj.poll',
    'socialauth',
    'openid_consumer',
    'sentry',
    'sentry.client',
    'memcache_status',
    'djcelery',
    'registration',
    'uni_form',
    'django_extensions',
    'south',
    'haystack',
    'threadedcomments',
    'custom_threadedcomments',
)

COMMENTS_APP = 'custom_threadedcomments'

## HAYSTACK ##
HAYSTACK_CONNECTIONS = {
    'default': {
        # For Solr:
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8090/solr/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
    },
} 
## END HAYSTACK ###

##REGISTRATION
ACCOUNT_ACTIVATION_DAYS = 1
## END REG

### SESSION CACHING ##
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
### END SESSION CACHING

### BEGIN SOCIALAUTH ###
LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

from localsettings import *

#MIDDLEWARE_CLASSES += LOCAL_SETTINGS_MIDDLEWARE

from socialauth_settings import *

### END SOCIALAUTH ###

import logging
from sentry.client.handlers import SentryHandler

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()# ensure we havent already registered the handler
if SentryHandler not in map(lambda x: x.__class__, logger.handlers):
    logger.addHandler(SentryHandler())

    # Add StreamHandler to sentry's default so you can catch missed exceptions
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())

import sys

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
    CACHES = {}
    MIDDLEWARE_CLASSES = (
        #'johnny.middleware.LocalStoreClearMiddleware',
        #'johnny.middleware.QueryCacheMiddleware',
        #'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'openid_consumer.middleware.OpenIDMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'sentry.client.middleware.Sentry404CatchMiddleware',
    )


