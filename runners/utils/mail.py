# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import settings
from sendgrid.helpers.mail import *


def send_mail(subject, message):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email("suporte@bonde.org")
    to_email = Email(settings.SENDGRID_SEND_EMAIL)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
