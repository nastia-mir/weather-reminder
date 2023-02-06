import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherreminderproject.settings")

app = Celery("weatherreminderproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'send-scheduled-email-1': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/1'),
        'args': [1],
    },
    'send-scheduled-email-3': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/3'),
        'args': [3],
    },
    'send-scheduled-email-6': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/6'),
        'args': [6],
    },
    'send-scheduled-email-12': {
        'task': 'send_scheduled_email',
        'schedule': crontab(hour='*/12'),
        'args': [12],
    },


    'send-scheduled-webhook-1': {
        'task': 'send_scheduled_webhook',
        'schedule': crontab(hour='*/1'),
        'args': [1],
    },
    'send-scheduled-webhook-3': {
        'task': 'send_scheduled_webhook',
        'schedule': crontab(hour='*/3'),
        'args': [3],
    },
    'send-scheduled-webhook-6': {
        'task': 'send_scheduled_webhook',
        'schedule': crontab(hour='*/6'),
        'args': [6],
    },
    'send-scheduled-webhook-12': {
        'task': 'send_scheduled_webhook',
        'schedule': crontab(hour='*/12'),
        'args': [12],
    },


    'update-weather': {
        'task': 'update_weather',
        'schedule': crontab(minute='*/10'),
    }
}

app.autodiscover_tasks()



