#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply migrations
echo "Apply migrations"
python manage.py migrate

# Add seed data
echo "Add seed data"
python manage.py initialize_app

# Start server
echo "Starting server"
/usr/local/bin/gunicorn rooming.wsgi:application -w 2 -b :8000 --reload
