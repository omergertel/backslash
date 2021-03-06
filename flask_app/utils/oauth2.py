import logbook

from flask import current_app, request
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow


_logger = logbook.Logger(__name__)


def get_oauth2_identity(auth_code):

    client_id = current_app.config.get('OAUTH2_CLIENT_ID')
    client_secret = current_app.config.get('OAUTH2_CLIENT_SECRET')
    if not client_id:
        _logger.error('No OAuth2 client id configured')
        return

    if not client_secret:
        _logger.error('No OAuth2 client secret configured')
        return

    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,

        scope='https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri=request.host_url[:-1])

    credentials = flow.step2_exchange(auth_code)

    info = _get_user_info(credentials)
    _logger.debug('Found user info: {}', info)
    return info


def _get_user_info(credentials):
    http_client = Http()
    if credentials.access_token_expired:
        credentials.refresh(http_client)
    credentials.authorize(http_client)
    service = build('oauth2', 'v2', http=http_client)
    return service.userinfo().get().execute()
