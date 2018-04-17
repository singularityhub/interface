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
from tunel.views.plugins import generate_plugins
from sregistry.utils import read_file

import os
import pwd
import json
import logging

# SECURITY #####################################################################

@app.after_request
def inject_csrf_token(response):
    response.headers.set('X-CSRF-Token', generate_csrf())
    return response


# LOGGING ######################################################################

name = app.config.get('ROBOTNAME')
file_handler = logging.FileHandler("/tmp/tunel-server-%s.log" %name)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)  

@app.route('/logs', methods=['POST'])
def logs(content=''):
    '''return a plain text log to parse into any view for the user
    '''

    logfile = '/tmp/tunel-server-%s.log' %app.config.get('ROBOTNAME')
    if os.path.exists(logfile):
        content = read_file(logfile)

    if not isinstance(content,list):
        content=[content]

    # Add the name of the log as the first line
    content=[logfile + '\n']+content

    return Response(content, status=200, mimetype='text/plain')


# PLUGINS ######################################################################

@app.context_processor
def add_plugins():
    return dict(plugins=generate_plugins())


# Main #########################################################################

@app.route('/')
def index():
    images = app.sregistry.images()
    return render_template('main/index.html', images=images)
