from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery.utils.log import get_task_logger

from weatherreminderproject.celery import app

from weatherapp.models import MyUser, Subscription
from weatherapp.services import WeatherReport

logger = get_task_logger(__name__)


@app.task(name='send_scheduled_email')
def send_scheduled_email(notification):
    cities = list(Subscription.objects.filter(notification=notification).all())

    emails = {}
    for subscription in cities:
        if not subscription.user.email in emails:
            emails[subscription.user.email] = [subscription]
        else:
            emails[subscription.user.email].append(subscription)

    for user in emails:
        email_data = {'weather': WeatherReport.get_weather(emails[user])}
        subject = 'Weather'
        message = render_to_string("reminder_email.html", email_data)
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user])
        email.send(fail_silently=False)
    logger.info("Emails sent")


@app.task(name='update_weather')
def update_weather():
    WeatherReport.update_weather()
    logger.info("Weather updated")
