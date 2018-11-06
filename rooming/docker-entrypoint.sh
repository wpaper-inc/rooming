#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
/usr/local/bin/gunicorn rooming.wsgi:application -w 2 -b :8000 --reload
