from __future__ import absolute_import, unicode_literals

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from weatherapp.celery import app

logger = get_task_logger(__name__)


@app.task(name='send_email_subscribed_task')
def send_email_subscribed_task(email, data):
    logger.info("Sent email")

    subject = 'Successfully subscribed'
    message = render_to_string("email_template.txt", data)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
