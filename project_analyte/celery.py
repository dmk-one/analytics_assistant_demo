import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_analyte.settings.local')

app = Celery('project_analyte')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

