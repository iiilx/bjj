#!/bin/sh

PROJECT_ROOT=/srv/www/bjj

cd $PROJECT_ROOT
python manage.py update_index
