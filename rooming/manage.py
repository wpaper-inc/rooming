#!/usr/bin/env python
import os
from os.path import join, dirname
from dotenv import load_dotenv
import sys

if __name__ == '__main__':
    if os.getenv('ENVIRON', 'develop') == 'develop':
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rooming.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
