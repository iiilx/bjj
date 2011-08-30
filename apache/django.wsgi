import os
import sys
#sys.path.append(os.path.abspath('../..'))
#sys.path.append(os.path.abspath('..'))
sys.path.append('/srv/www/bjj_project/staging')
sys.path.append('/srv/www/bjj_project/staging/bjj')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bjj.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


