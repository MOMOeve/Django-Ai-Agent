"""
ASGI config for cfehome project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from cfehome.utf8_bootstrap import configure_utf8

configure_utf8()

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')

application = get_asgi_application()
