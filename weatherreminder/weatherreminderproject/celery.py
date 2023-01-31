import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherreminderproject.settings")

app = Celery("weatherreminderproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'send-scheduled-1': {
        'task': 'weatherapp.tasks.send_scheduled',
        'schedule': 15,
    }
}


app.autodiscover_tasks()



