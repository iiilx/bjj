import os

os.environ['DJANGO_SETTINGS_MODULE'] = "hntagged.settings"

import sys
sys.path.append('/srv/www')
sys.path.append('/srv/www/hntagged')

import logging
import datetime 

from django.template import Context, Template, loader, RequestContext
from django.db.models import Avg
from django.core.management import setup_environ
from hntagged import settings
setup_environ(settings)

from hntagged import urls
from hn.models import Post, Category
from db_analyzer.models import Record, DayRecord
logger = logging.getLogger()

def create_avg():
    yesterday = datetime.date.today() - datetime.timedelta(1) 
    today = datetime.date.today()
    view_names = [p.name for p in urls.urlpatterns[3:]]
    data=[]
    for name in view_names:
        avgs = Record.objects.filter(view_name = name, dt__range = (datetime.datetime.combine(today, datetime.time.min),datetime.datetime.combine(today, datetime.time.max))).aggregate(Avg('queries'), Avg('time'))
        data.append((name, avgs['queries__avg'], avgs['time__avg']))
    data.sort(key=lambda tup: tup[2], reverse=True)
    print data

if __name__ == '__main__':
    create_avg()
