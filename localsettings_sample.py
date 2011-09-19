DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

LOGIN_REDIRECT_URL = '/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

## HAYSTACK ##
HAYSTACK_CONNECTIONS = {
    'default': {
        # For Solr:
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8090/solr3/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
    },
} 
## END HAYSTACK ###

CACHES = {
    'default' : dict(
        BACKEND = 'johnny.backends.memcached.MemcachedCache',
        LOCATION = ['127.0.0.1:11211'],
        JOHNNY_CACHE = True,
        KEY_PREFIX = 'sbjj'
    )
}

### BEGIN JOHNNYCACHE ###
JOHNNY_MIDDLEWARE_KEY_PREFIX='bjj2'
JOHNNY_TABLE_BLACKLIST = (
    'bjj_post',
    'auth_user',
)
### END JOHHNCACHE ###


#EMAIL SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'exmaple@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL='exmaple@gmail.com'
## END EMAIL

### DOMAIN SETTINGS ###
SITE_DOMAIN = 'bjj.example.com'
## end domain settings ###
DOMAIN = SITE_DOMAIN

LOCAL_SETTINGS_MIDDLEWARE = ('app.middleware.WhiteList',)

INTERNAL_IPS = ('69.181.70.85')
