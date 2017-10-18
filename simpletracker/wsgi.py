"""
WSGI config for simpletracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

from simpletracker.settings import DEBUG

if DEBUG:
    import os

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpletracker.settings")

    application = get_wsgi_application()
else:
    import os
    import sys

    sys.path.append('/opt/bitnami/apps/django/django_projects/si_tracker')
    os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/si_tracker/egg_cache")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpletracker.settings")

    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
