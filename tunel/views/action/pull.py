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

import json
import logging
import os


@app.route('/action/pull')
def action_pull():
    '''the fetch view to perform the pull, and return a response
    '''

    # Ensure uri appears once

    container = request.args.get('q')
    uri = request.args.get('uri')
    container = '%s%s' %(uri, container.replace(uri,''))

    app.logger.info("PULL for %s" %container)

    # Make sure we use the right client
    os.environ['SREGISTRY_CLIENT'] = uri.replace('://','')
    os.environ.putenv('SREGISTRY_CLIENT', uri.replace('://',''))
    from sregistry.main import get_client
    client = get_client(image=container)
    
    try:
        image_file = client.pull(container, force=True)
    except:
        image_file = '''ERROR: manifest unknown, or pull error. 
                        Use docker-compose logs web to see issue!'''
        
    return Response(image_file, mimetype='text/plain')


@app.route('/pull')
def pull():
    '''the main pull view to show a terminal, and allow a client to pull
    '''
    app.sregistry.client_name = 'nvidia'
    nvidia = app.sregistry._get_setting('SREGISTRY_NVIDIA_TOKEN')
    return render_template('action/pull.html', nvidia=nvidia)
