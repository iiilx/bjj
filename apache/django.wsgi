import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../../..')))
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'bjj.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


