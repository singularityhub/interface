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
from spython.main import Client

import json
import itertools
import logging
import os


@app.route('/action/pull', methods=['POST'])
def action_pull():
    '''the fetch view to perform the pull, and return a response
    '''

    # Ensure uri appears once
    container = request.form.get('uri') # ubuntu:latest
    uri = request.form.get('endpoint')  # docker://
    container = '%s%s' %(uri, container.replace(uri,''))

    app.logger.info("PULL for %s" %container)

    # We will stream the response back!
    image, puller = Client.pull(container, stream=True, pull_folder='/tmp')
    puller = itertools.chain(puller, [image])
        
    return Response(puller, mimetype='text/plain')


@app.route('/action/add', methods=['POST'])
def action_add():
    '''add a finished image to the client.
    '''
    data = json.loads(request.data.decode('utf-8'))
    container = data.get('container')
    uri = data.get('uri')

    if container not in ['', None]:
        if os.path.exists(container):
            app.logger.info('ADD %s' %container)
            container = app.sregistry.add(image_uri=uri, 
                                          image_path=container)
            container = container.name
                 
    message = {'container': container, 'uri': uri }
    return jsonify({"data": message })



@app.route('/pull')
def pull():
    '''the main pull view to show a terminal, and allow a client to pull
    '''
    app.sregistry.client_name = 'nvidia'
    nvidia = app.sregistry._get_setting('SREGISTRY_NVIDIA_TOKEN')
    return render_template('action/pull.html', nvidia=nvidia)
