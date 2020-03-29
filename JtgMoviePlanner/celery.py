import os
from JtgMoviePlanner import settings
from celery import Celery

# Setting the Default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JtgMoviePlanner.settings')
app = Celery('JtgMoviePlanner')

# Using a String here means the worker will always find the configuration information
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
