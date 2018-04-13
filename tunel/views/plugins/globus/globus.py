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

from globus_sdk.exc import TransferAPIError
from .utils import (
    do_transfer,
    generate_transfer_file,
    generate_transfer_name
)

from sregistry.main import get_client
from tunel.server import app

import globus_sdk
import json
import logging
import os
import re
import requests

## Transfer views

@app.route('/globus/transfer/get/<endpoint_id>', methods=['POST'])
def globus_transfer_from(endpoint_id, message="Invalid request."):
    '''transfer one or more containers from the tunel registry endpoint to a 
       selected globus endpoint.

       Parameters
       ==========
       endpoint_id: the id of the endpoint to transfer from.
       message: the default message sent to the user if the transfer 
                request had an issues.

    '''

    init_globus_client()

    # Do we need to update tokens?
    if app.globus_client._tokens_need_update():
        return globus()

    if not hasattr(app.globus_client, 'transfer_client'):
        app.globus_client._init_transfer_client()

    # The tunel interface local endpoint
    dest = app.config['PLUGIN_GLOBUS_ENDPOINT']

    # Post indicates browsing the tree, with an additional path to parse
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        remote = data.get('remote', '')
        
        tmp = generate_transfer_name()

        result = do_transfer(client=app.globus_client,
                             source_endpoint=endpoint_id,
                             dest_endpoint=dest,
                             images=[(remote, tmp)]) # [(source, dest)...]

        link = "https://globus.org/app/activity/%s" %result['task_id']
        mess = result['message']
        message = "%s: <a target='_blank' href='%s'>view task</a>" %(mess, link)

    return jsonify({"data": message })



@app.route('/globus/transfer/put/<endpoint_id>', methods=['POST'])
def globus_transfer_to(endpoint_id, message="Invalid request."):
    '''transfer one or more containers from the tunel registry endpoint to a 
       selected globus endpoint.

       Parameters
       ==========
       endpoint_id: the id of the endpoint to transfer to.
       message: the default message sent to the user if the transfer did
                not have any containers, or wasn't a post (we should
                not get to the second of those states).

    '''

    init_globus_client()

    # Do we need to update tokens?
    if app.globus_client._tokens_need_update():
        return globus()

    if not hasattr(app.globus_client, 'transfer_client'):
        app.globus_client._init_transfer_client()

    # The tunel interface local endpoint
    source_endpoint = app.config['PLUGIN_GLOBUS_ENDPOINT']

    # Post indicates browsing the tree, with an additional path to parse
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        path = data.get('path', '').replace('/~/','')
        containers = data.get('containers', [])
        
        for container in containers:

            # Create temporary file
            tmp = generate_transfer_file(container)
            image = os.path.join(path, os.path.basename(container))
            images.append([tmp, image])

        # Submit image set as one job
        result = do_transfer(client=app.globus_client,
                             source_endpoint=source_endpoint,
                             dest_endpoint=endpoint_id,
                             images=images)

        link = "https://globus.org/app/activity/%s" %result['task_id']
        mess = result['message']
        message = "%s: <a target='_blank' href='%s'>view task</a>" %(mess, link)

    return jsonify({"data": message })


@app.route('/globus/<endpoint_id>', methods=['GET', 'POST'])
def get_endpoint(endpoint_id, path='', message=None, json_response=False):
    '''return a single endpoint that matches the result of a query, meaning
       a detail page that shows files within. This should be an endpoint
       detail page (not sure how should look)
    '''
    init_globus_client()

    # Do we need to update tokens?
    if app.globus_client._tokens_need_update():
        return globus()

    if not hasattr(app.globus_client, 'transfer_client'):
        app.globus_client._init_transfer_client()

    # Post indicates browsing the tree, with an additional path to parse
    if request.method == "POST":
        json_response = True
        path = request.args.get('path') or None

    # Get a list of files at endpoint, under specific path

    try:
        endpoint = app.globus_client._get_endpoint(endpoint_id)
        paths = app.globus_client.transfer_client.operation_ls(endpoint_id, 
                                                        path=path).data
        
    # Pull out call from sregistry to return view with error

    except TransferAPIError as message:
        return get_endpoints(term=term, message=message)
        
    # JSON response for POSTs

    if json_response is True:
        return jsonify({'data': paths['DATA'], 
                        'path': paths['path'] })

    images = app.sregistry.images()

    return render_template('plugins/globus/endpoint.html', 
                                endpoint=endpoint,
                                paths=paths['DATA'],
                                path=paths['path'],
                                images=images,
                                activeplugin="globus")



def get_endpoints(term=None, message=None, endpoints=None):
    '''return a single endpoint that matches the result of a query, meaning
       a detail page that shows files within. This should be an endpoint
       detail page (not sure how should look)
    '''
    return render_template('plugins/globus/index.html', message=message,
                                                        endpoints=endpoints,
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
        term = request.form.get('term') or None
        
    # Check if client tokens need an update

    if not app.globus_client._tokens_need_update():

        # needs_update will prompt the user to issue update command
        needs_update = False

        # If the user has provided a query, only return those with scope "all"
        scopes = None
        if term is not None:
            scopes = "all"

        # Dictionary of endpoints, keys are scope
        endpoints = app.globus_client._get_endpoints(term)
        endpoints = parse_endpoints(endpoints, scopes=scopes)

        # If no endpoints, tell user no results
        if len(endpoints) == 0 and term:
            term = "No results for %s" %term

    return render_template('plugins/globus/index.html', term=term, 
                                                        endpoints=endpoints,
                                                        needs_update=needs_update,
                                                        activeplugin="globus")



# Helpers

def parse_endpoints(endpoints, scopes=None):
    '''parse endpoints into a table. If no scope provided, use all.

       Parameters
       ==========
       endpoints: dictionary of endpoints, keys are scope, values list of ep.
       scopes: list of keys for endpoints. If None, use all

       row:
       [id][scope][display_name][contact_email][organization]     

       For display logic for status, see 
       //github.com/globus/globus-sdk-python/issues/286#issuecomment-380465278

    '''
    if scopes is None:
        scopes = list(endpoints.keys())

    rows = []
    for kind,eps in endpoints.items():
        if kind in scopes:
            for epid,epmeta in eps.items():

               # setup incomplete: is_globus_connect globus_connect_setup_key
               #if not epmeta['globus_connect_setup_key']:
               #    status = "setup incomplete"
  
               name = epmeta['display_name'] or epmeta['canonical_name']
               row = {'id': epid,
                      'kind': kind,
                      'name': name,
                      'email': epmeta['contact_email'],
                      'org': epmeta['organization'],
                      'active': epmeta['activated'],
                      'public': epmeta['public'],
                      'gc': epmeta['is_globus_connect']}

               rows.append(row)
    return rows


def init_globus_client():
    '''return a globus client with an up to date credential, or update. If the
       token isn't updated, the user will be prompted to issue a command
       to the container to do so.
    '''

    if not hasattr(app, 'globus_client'):
        app.globus_client = get_client('globus://')
