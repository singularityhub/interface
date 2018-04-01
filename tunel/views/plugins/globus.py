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

from tunel.server import app

import logging
import os
import json


@app.route('/globus/<endpoint_id>')
def get_endpoint(endpoint_id):

    from sregistry.main import get_client
    client = get_client('globus://')
    endpoint = client._list_endpoints(endpoint_id)
    return render_template('plugins/globus/index.html', endpoints=endpoints,
                                                        activeplugin="globus")

@app.route('/globus')
def globus():

    # Default globus should show endpoints
    from sregistry.main import get_client
    client = get_client('globus://')
    endpoints = client._list_endpoints()
    return render_template('plugins/globus/index.html', endpoints=endpoints,
                                                        activeplugin="globus")
