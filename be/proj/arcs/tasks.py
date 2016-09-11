from __future__ import absolute_import
import os
import celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

# from django.conf import settings

# app = celery.Celery('tasks')

# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task
# def add(x, y):
#     return x + y

# @app.task
# def attachments()