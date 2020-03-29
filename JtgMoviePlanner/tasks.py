from celery import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from . import settings

@task()
def send_verify_email_task(email_subject, email, token):
    msg_html = render_to_string('templates/email_template.html', {'token': token, 'url': settings.URL})
    msg = ""
    return send_mail(
        email_subject,
        msg,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=msg_html
    )
       