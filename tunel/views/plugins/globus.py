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
    session,
    Response,
    jsonify
)

from sregistry.main import get_client
from tunel.server import app

import logging
import os
import json


@app.route('/globus/<endpoint_id>')
def get_endpoint(endpoint_id):
    '''return a single endpoint that matches the result of a query, meaning
       a detail page that shows files within. This should be an endpoint
       detail page (not sure how should look)
    '''
    client = get_client('globus://')

    # Option 2: An endpoint without query will just list containers there
    endpoint = client._list_endpoint(endpoint_id)
    return render_template('plugins/globus/index.html', endpoints=[endpoint],
                                                        activeplugin="globus")

@app.route('/globus')
def globus():
    '''the main globus view that lists all endpoints the user has shared with
       them, or owns.
    '''
    # Option 1: No query or endpoints lists all shared and personal
    return endpoint_table()



@app.route('/globus', methods=['POST'])
def search_endpoints():
    '''search endpoints with a term, also returning the user "my-endpoints"
       and "shared-with-me" scope
    ''''
    # Default globus should show endpoints
    client = get_client('globus://')

    term = None
    if request.method == "POST":
        term = request.form.get('term')

    # Return the endpoints for the user
    return endpoint_table(term)



def endpoint_table(term=None):
    '''common view to return endpoints with table
    
       Parameters
       ==========
       term: a search term to query the table, or None to show all endpoints
       in the user's shared-with-me or my-endpoints
    '''

    # Default globus should show endpoints
    client = get_client('globus://')
    endpoints = client._list_endpoints(term)
    return render_template('plugins/globus/index.html', endpoints=endpoints,
                                                        activeplugin="globus")

