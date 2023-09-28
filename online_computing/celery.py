from __future__ import absolute_import, unicode_literals

import os
import sys

from django.conf import settings
from celery import Celery
from celery.utils.log import get_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_computing.settings')

logger = get_task_logger(__name__)

math_computing_app = Celery('math_computing')

math_computing_app.config_from_object('django.conf:settings', namespace='CELERY')

math_computing_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

sys.set_int_max_str_digits(0)
