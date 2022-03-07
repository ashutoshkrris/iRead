from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_custom_email(receiver_email, subject, sender_email, sender_name, template_name, **kwargs):
    html_content = render_to_string(f"emails/{template_name}", kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        f"{sender_name} <{sender_email}>",
        [receiver_email]
    )
    email.attach_alternative(html_content, "text/html")
    EmailThread(email).start()
