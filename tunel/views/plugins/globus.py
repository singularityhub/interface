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
def globus(term=None, needs_update=True, endpoints=None):
    '''This is the primary globus view. If the client isn't updated, the user is
       given a command to execute to the container to update the tokens. The
       default view, given a token, will return a view of all endpoints
       for the user with scopes "my-endpoints" and "shared-with-me"
    '''

    init_globus_client()

    if request.method == "POST":
        term = request.form.get('term')
        
    # Check if client tokens need an update

    if not app.globus_client._tokens_need_update():

        # needs_update will prompt the user to issue update command
        needs_update = False
        endpoints = app.globus_client._list_endpoints(term)
    
    return render_template('plugins/globus/index.html', term=term, 
                                                        endpoints=endpoints,
                                                        needs_update=needs_update,
                                                        activeplugin="globus")



# Helpers

def init_globus_client():
    '''return a globus client with an up to date credential, or update. If the
       token isn't updated, the user will be prompted to issue a command
       to the container to do so.
    '''

    if not hasattr(app, 'globus_client'):
        app.globus_client = get_client('globus://')
