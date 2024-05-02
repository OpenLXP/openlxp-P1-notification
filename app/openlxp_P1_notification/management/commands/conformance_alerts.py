import json
import logging

import requests

from requests.auth import AuthBase

from django.core.management.base import (BaseCommand, CommandParser,
                                         CommandError)
from django.core.mail import EmailMessage
from botocore.exceptions import ClientError

from openlxp_P1_notification.models import (email)

from openlxp_P1_notification.serializer import EmailSerializer

logger = logging.getLogger('dict_config_logger')


class TokenAuth(AuthBase):
    """Attaches HTTP Authentication Header to the given Request object."""

    def __call__(self, r, token_name='EMAIL_AUTH'):
        # modify and return the request

        r.headers[token_name] = 'ECXL3TLMFVHDTGMKDREVP457YI'
        return r


def send_email(email_type, template_inputs):
    """Command to trigger email notification"""
    # print(email_type.subject)
    # print(email_type.reference)
    # print(email_type.template_type.template_body)
    # # print(email_type.template_body)
    # print(list(email_type.recepients.values_list("email_address", flat=True)))
    # print(email_type.sender)

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    # SENDER = email_type.sender

    # # Replace recipient@example.com with a "To" address. If your account
    # # is still in the sandbox, this address must be verified.
    # RECIPIENT = list(email_type.recipients.values_list("email_address",
    #                                                    flat=True))

    # # The subject line for the email.
    # SUBJECT = email_type.subject

    # # The HTML body of the email.
    # BODY_HTML = email_type.template_type.template_body

    # for each_recipient in RECIPIENT:
    #     try:
    #         # Provide the contents of the email.
    #         mail = EmailMessage(SUBJECT, BODY_HTML, SENDER,
    #                             [each_recipient])
    #         mail.content_subtype = "html"

    #         # mail.send()
    #     # Display an error if something goes wrong.
    #     except ClientError as e:
    #         logger.error(e.response['Error']['Message'])
    #         continue

    body_data = EmailSerializer(email_type).data

    body_data["template_inputs"] = template_inputs
    body_data = json.dumps(body_data)

    headers = {'Content-Type': 'application/json'}

    jar = requests.cookies.RequestsCookieJar()
    jar.set('__Host-p1ps-staging-authservice-session-id-cookie',
            'NlnUUosv8pQF85lKSwoFfVUjwbqy57Uskh1Mt9JJJ9pfwxqjk0h98tFooSfdvRvk',
            domain='p1ps-il2.staging.dso.mil', path='/')

    P1_response = requests.post(url='https://p1ps-il2.staging.dso.mil/api/teams/IPKRGXU5RFEUNPJSNXWBGBSBNE/emails/edlm-status-update',
                                data=body_data, headers=headers,
                                auth=TokenAuth(), cookies=jar)

    print(P1_response.text)


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument('email_references', nargs="+", type=str)
        parser.add_argument('email_references', type=str)
        # return super().add_arguments(parser)

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        # for email_reference in options['email_references']:
        try:
            email_type = email.objects.get(
                reference=options['email_references'])
        except email.DoesNotExist:
            raise CommandError('Email Reference "%s" does not exist' %
                               options['email_references'])
        template_inputs = {
                                        "datetime": "2024-01-01",
                                        "name": "Karen Ann Jijo"
                                }
        send_email(email_type, template_inputs)
