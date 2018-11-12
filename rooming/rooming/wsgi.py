"""
WSGI config for rooming project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rooming.settings')

application = get_wsgi_application()
application = newrelic.agent.wsgi_application()(application)
