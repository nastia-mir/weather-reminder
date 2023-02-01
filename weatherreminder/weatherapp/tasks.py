from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery.utils.log import get_task_logger
from celery.schedules import crontab

from weatherreminderproject.celery import app

from weatherapp.models import MyUser, Subscription
from weatherapp.services import WeatherReport

logger = get_task_logger(__name__)


def send_email(email_data):
    subject = 'Successfully subscribed'
    message = render_to_string("email_template.html", email_data)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email_data['email']])
    return email.send(fail_silently=False)


@app.task(name='send_email_subscribed_task')
def send_email_subscribed_task(email_data):
    logger.info("Sent email")
    return send_email(email_data)


@app.task(name='send_scheduled_email')
def send_scheduled_email(notification):
    logger.info("Sent email")

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
        message = render_to_string("test_email.html", email_data)
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user])
        email.send(fail_silently=False)
