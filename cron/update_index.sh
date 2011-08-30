#!/bin/sh

PROJECT_ROOT=`dirname $PWD`
cd $PROJECT_ROOT
python manage.py update_index
