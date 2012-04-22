import logging
from Acquisition import aq_parent
from euphorie.client.api.authentication import EuphorieAPIPlugin
from euphorie.client.api.entry import API
from euphorie.client.setuphandlers import add_api_authentication_plugin


log = logging.getLogger(__name__)


def add_client_api(context):
    siteroot = aq_parent(context)
    client = siteroot.client
    if 'api' in client:
        log.info('Client API already configured.')
        return

    log.info('Enabling client API.')
    client['api'] = API('api')


def add_api_authentication(context):
    siteroot = aq_parent(context)
    pas = siteroot.acl_users
    if pas.objectIds([EuphorieAPIPlugin.meta_type]):
        log.info('API authentication plugin already installed.')
        return

    add_api_authentication_plugin(pas)
