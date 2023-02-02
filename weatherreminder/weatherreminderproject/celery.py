import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherreminderproject.settings")

app = Celery("weatherreminderproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'send-scheduled-1': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/1'),
        'args': [1],
    },
    'send-scheduled-3': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/3'),
        'args': [3],
    },
    'send-scheduled-6': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/6'),
        'args': [6],
    },
    'send-scheduled-12': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/12'),
        'args': [12],
    },


}

app.autodiscover_tasks()



