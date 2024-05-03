import logging
import os

import requests

from requests.auth import AuthBase

logger = logging.getLogger('dict_config_logger')

headers = {'Content-Type': 'application/json'}


"""
    Functions set up to extract environment values for
    Platform One Postal Service (P1PS) API

"""


def get_P1PS_base_endpoint():
    """Extracts P1PS base endpoint"""
    P1PS_endpoint = "https://" + os.environ.get('P1PS_DOMAIN')

    if P1PS_endpoint[0]:
        logger.info("P1PS endpoint value  is present and set")
    else:
        logger.error("P1PS endpoint value is absent and not set")

    return P1PS_endpoint


def get_P1PS_team_token():
    """Extracts P1PS base endpoint"""
    team_token = os.environ.get('TEAM_TOKEN')

    if team_token[0]:
        logger.info("Team Token value  is present and set")
    else:
        logger.error("Team Token value is absent and not set")

    return team_token


def get_P1PS_team_ID():
    """Extracts P1PS base endpoint"""
    team_token = os.environ.get('TEAM_ID')

    if team_token[0]:
        logger.info("Team ID value  is present and set")
    else:
        logger.error("Team ID value is absent and not set")

    return team_token


"""
    Configuration set up for Platform One Postal Service (P1PS)
    API requests

"""


class TokenAuth(AuthBase):
    """Attaches HTTP Authentication Header to the given Request object."""

    def __call__(self, r, token_name='EMAIL_AUTH'):
        # modify and return the request

        r.headers[token_name] = get_P1PS_team_token()
        return r


def SetCookies():
    """Sets requests cookies jar with P1 authorization cookies"""

    jar = requests.cookies.RequestsCookieJar()
    jar.set(os.environ.get('COOKIE_NAME'),
            os.environ.get('COOKIE_VALUE'),
            domain=os.environ.get('P1PS_DOMAIN'), path='/')

    return jar


def SendResponse(response):
    """Function to return response and error catches"""

    if response.status_code in [400, 401, 404, 500]:
        logger.error(response.json)
    elif response.status_code in [200, 201]:
        try:
            logger.info(response.json())
        except requests.RequestException:
            logger.warning(requests.RequestException)


"""
    Requests set up using Platform One Postal Service (P1PS)
    API Specification (1.0.0)

"""


def overall_health():
    """Request to perform P1PS health check """
    base_endpoint = get_P1PS_base_endpoint()

    url = base_endpoint + "/api/health"

    response = requests.get(url=url, headers=headers,
                            auth=TokenAuth(), cookies=SetCookies())
    SendResponse(response)


def send_email(body_data, template_type):
    """Request to send email via P1PS"""

    base_endpoint = get_P1PS_base_endpoint()
    team_id = get_P1PS_team_ID()

    url = base_endpoint + "/api/teams/" + team_id + "/emails/" + template_type

    response = requests.post(url=url, headers=headers,
                             data=body_data, auth=TokenAuth(),
                             cookies=SetCookies())
    SendResponse(response)
