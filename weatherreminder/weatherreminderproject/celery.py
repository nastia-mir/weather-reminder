import os
import json

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherreminderproject.settings")

app = Celery("weatherreminderproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'send-scheduled-1': {
        'task': 'weatherapp.tasks.send_scheduled_email',
        'schedule': crontab(minute='*/1'),
        'args': json.dumps([1]),
    }
}


app.autodiscover_tasks()



