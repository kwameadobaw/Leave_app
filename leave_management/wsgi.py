"""WSGI config for leave_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Check if running on Vercel
if 'VERCEL' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_management.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_management.settings')

application = get_wsgi_application()

app = application
