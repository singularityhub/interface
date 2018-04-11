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

# PLUGINS ######################################################################

@app.context_processor
def add_plugins():
    return dict(plugins=generate_plugins())


# Main #########################################################################

@app.route('/')
def index():
    images = app.sregistry.images()
    return render_template('main/index.html', images=images)
