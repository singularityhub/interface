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

from flask_wtf.csrf import generate_csrf
from flask_cors import cross_origin
from werkzeug import secure_filename

from tunel.server import app

import logging
import os
import json


# LOGGING ######################################################################

file_handler = logging.FileHandler("/code/tunel-server.log")
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

# SECURITY #####################################################################

@app.after_request
def inject_csrf_token(response):
    response.headers.set('X-CSRF-Token', generate_csrf())
    return response
  

# Main #########################################################################

@app.route('/')
def index():
    images = app.sregistry.images()
    return render_template('index.html', images=images)



# Containers ###################################################################

@app.route('/container/<container>')
def get_container(container):
    links = get_container_links(container) 
    args = get_container_args(app.containers[container],cli=app.cli)
    labels = get_container_labels(app.containers[container],cli=app.cli)
    return render_template('container.html', container=container,
                                             links=links,
                                             args=args,
                                             labels=labels)


@app.route('/container', methods=['GET','POST'])
def container():
    '''POST view to see a container from a form'''  
    if request.method == 'POST':
        container = request.form['container']
        return get_container(container)
    return index()


@app.route('/container/run/<container>')
def run_container(container):

    if container in app.containers:
        image_path = app.containers[container]
        cargs = get_container_args(image_path,cli=app.cli)

        contenders = list(request.args.keys())
        args = []

        for contender in contenders:
            value = sanitize(request.args.get(contender))
            flag = "--%s" %(contender)
            found = False

            if 'bool' in cargs:
                if contender in cargs['bool']:
                    args.append(flag)

            if 'str' in cargs and not found:
                if contender in cargs['str']:
                    args = args + [flag,'"%s"' %value]
                    found = True

            if 'int' in cargs and not found:
                if contender in cargs['int']:
                    args = args + [flag,str(int(value))]
                    found = True

            if 'float' in cargs and not found:
                if contender in cargs['float']:
                    args = args + [flag,str(float(value))]

        if len(args) == 0:
            args = None

        result = runc(image_path,args=args,cli=app.cli)

        # Dictionary gets rendered as json
        if isinstance(result,dict):
            return jsonify(result)    

        # Otherwise text
        return result


    # Not a value container, return to index  
    return index()
