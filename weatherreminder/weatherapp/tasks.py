from __future__ import absolute_import, unicode_literals

from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task


@shared_task(name='send_email_subscribed_task')
def send_email_subscribed_task(data):
    print("send email")

    subject = 'Email confirmation'
    message = render_to_string("email.html", {
        'user': user,
        'domain': get_current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.user_id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
