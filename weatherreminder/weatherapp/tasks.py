from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery.utils.log import get_task_logger

from weatherreminderproject.celery import app

logger = get_task_logger(__name__)


def send_email(email_data):
    subject = 'Successfully subscribed'
    message = render_to_string("email_template.txt", email_data)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email_data['email']])
    return email.send(fail_silently=False)


@app.task(name='send_email_subscribed_task')
def send_email_subscribed_task(email_data):
    logger.info("Sent email")
    print("task started")
    return send_email(email_data)


