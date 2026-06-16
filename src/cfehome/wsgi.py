"""
WSGI config for cfehome project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from cfehome.utf8_bootstrap import configure_utf8

configure_utf8()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')

application = get_wsgi_application()
