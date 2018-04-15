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

import os
import json
import logging


@app.route('/container/<uri>', methods=['POST', 'GET'])
def view_container(uri=None, message=None, container=None):
    '''return a plain text log to parse into any view for the user
    '''
    if request.method == "POST":
        uri = request.form.get('container')

    elif request.method == "GET":
        uri = request.args.get('uri')

    if uri is not None:
        container = app.sregistry.get(uri)
        message = "Please select a container to view!"

    images = app.sregistry.images()
    return render_template('main/container.html', container=container,
                                                  message=message,
                                                  images=images)
