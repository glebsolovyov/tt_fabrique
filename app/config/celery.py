import os
import time

from celery import Celery
from core.configs.celery import CELERY_BROKER_URL
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('tt_fabrique')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_messages': 'apps.api.tasks.send_messages'
}