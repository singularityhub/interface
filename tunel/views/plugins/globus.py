'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017-2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from flask import (
    flash,
    render_template, 
    request,
    redirect,
    session,
    Response,
    jsonify,
    url_for
)

from sregistry.main import get_client
from tunel.server import app

import globus_sdk
import json
import logging
import os
import re
import pickle
import requests


@app.route('/globus/<endpoint_id>')
def get_endpoint(endpoint_id):
    '''return a single endpoint that matches the result of a query, meaning
       a detail page that shows files within. This should be an endpoint
       detail page (not sure how should look)
    '''
    return endpoint_table(endpoint_id=endpoint_id)


def get_endpoints(term=None):
    '''return a single endpoint that matches the result of a query, meaning
       a detail page that shows files within. This should be an endpoint
       detail page (not sure how should look)
    '''
    return endpoint_table(term=term)


def endpoint_table(term=None, endpoint_id=None):
    '''a shared view to take a term OR an endpoint id, and return a table view
    '''
    init_globus_client()

    # Do we need to update tokens?
    if app.globus_client._tokens_need_update():
        return globus()

    # Option 1: we have an endpoint id
    if endpoint_id is not None:
        endpoints = [app.globus_client._list_endpoint(endpoint_id)]
    else:
        endpoints = app.globus_client._list_endpoints(term)

    return render_template('plugins/globus/index.html', endpoints=endpoints,
                                                        activeplugin="globus")


@app.route('/globus', methods=['POST', 'GET'])
def globus(term=None, auth_uri=None, endpoints=None):
    '''This is the primary globus view. If the client isn't updated, the user is
       given an auth uri with a form to enter a code. If updated, the user can
       see an endpoint table and search endpoints with a 
       term, also returning the user "my-endpoints" and "shared-with-me" scope
    '''

    # Variables to pass on to view
    init_globus_client()

    if request.method == "POST":
        term = request.form.get('term')
        code = request.form.get('code')

        # If a code is provided, we've just posted and finished the login view
        if code not in ['', None]:
            pickle.dump(code, open('code.pkl','wb'))
            associate_user(code=code)
        
    # Check if client tokens need an update (in case we do, we give login form)
    if app.globus_client._tokens_need_update():
        auth_uri = generate_auth_uri()

    else:
        endpoints = app.globus_client._list_endpoints(term)
    
    return render_template('plugins/globus/index.html', term=term, 
                                                        endpoints=endpoints,
                                                        auth_uri=auth_uri,
                                                        activeplugin="globus")



# Helpers

def init_globus_client():
    '''return a globus client with an up to date credential, or update.
       The sregistry interface has an app key for globus different from the
       primary sregistry.
    '''

    if not hasattr(app, 'globus_client'):

        # Default globus should show endpoints
        client = get_client('globus://')
        client._client_id = "056ab436-e15b-4ead-b2c0-a3534f55d182"
        client._init_clients()

        # Redirect the user to the Globus code page
        redirect_uri = "https://auth.globus.org/v2/web/auth-code"

        # client._client is the Globus Client
        client._client.oauth2_start_flow(redirect_uri,
                                         refresh_tokens=True)
        app.globus_client = client


def generate_auth_uri():
    '''Generate a login uri to transfer the user to

       Parameters
       ==========
       client: the globus client, should already have correct token

    '''
    auth_uri = app.globus_client._client.oauth2_get_authorize_url()

    # We need to get rid of the scope, this is a bug
    auth_uri = re.sub("\&scope=.+auth-code",'', auth_uri)
    return auth_uri


def associate_user(code):
    ''' Here we do the following:

    1. Exchange the  code for refresh tokens. client._client is the globus
       client.
    2. Update the token infos in the credential cache

    Parameters
    ==========
    client: The sregistry client with Globus client at _client
    code: the code received from the post

    Returns
    =======
    client: The updated sregistry client, also updated for the app

    This function is intended to be called without returning a view, as
    the calling function can continue with an associated user. We have to do
    this because the Globus Python SDK redirect won't allow localhost with http
    '''

    # First step, get tokens from code
    tokens = app.globus_client._client.oauth2_exchange_code_for_tokens(code)
 
    auth = app.globus_client._load_config_token(tokens, 'auth')
    transfer = app.globus_client._load_config_token(tokens, token_type='transfer',
                      scope = "urn:globus:auth:scope:transfer.api.globus.org:all",
                      resource_server = "transfer.api.globus.org")
       
    # First priority: load from cache, use loaded above as default

    app.globus_client.auth = app.globus_client._get_and_update_setting(
                                                  'GLOBUS_AUTH_RESPONSE', auth)
    app.globus_client.transfer = app.globus_client._get_and_update_setting(
                                                   'GLOBUS_TRANSFER_RESPONSE',
                                                    transfer)
