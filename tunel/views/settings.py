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



# Settings #####################################################################

@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')


@app.route('/set/settings', methods=['GET'])
def set_settings():
    '''set a token for nvidia cloud. This should be a POST with csrf, okay
       with localhost for now
    '''
    token = request.args.get('nvidia')
    if token is not None:
        print(token)
        flash('Your Nvidia Token has been updated')
        app.sregistry.client_name = 'nvidia'
        app.sregistry._get_and_update_setting('SREGISTRY_NVIDIA_TOKEN', token)

    return Response(token, status=200, mimetype='application/json')
