from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

import string
import random


def send_email(to_email, template_name, subject, context):
    context.update({
        "BASE_URL": settings.WAGTAILADMIN_BASE_URL,
    })
    html_body = render_to_string(template_name, context)
    text_body = strip_tags(html_body)

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.FROM_EMAIL,
        to=[to_email],
        body=text_body
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))
