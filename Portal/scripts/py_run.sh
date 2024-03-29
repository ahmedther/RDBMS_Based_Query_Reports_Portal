#!/bin/sh

set -e


# python manage.py collectstatic --noinput

while true; do
  # Check if PostgreSQL server is available
  /py/bin/python /ehis_reports_portal/scripts/check_postgres.py

  if [ $? -eq 0 ]; then
    break  # Break the loop if connection successful
  fi

  sleep 1
done


# python manage.py runserver 0.0.0.0:9001

gunicorn --workers 3 --timeout 86400 --bind 0.0.0.0:8002 Portal.wsgi:application &

uwsgi --ini /ehis_reports_portal/uwsgi/uwsgi.ini
