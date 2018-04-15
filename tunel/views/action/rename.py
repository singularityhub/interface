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


@app.route('/action/rename', methods=['POST'])
def action_rename():
    '''the fetch view to rename the container, and return a response
    '''

    data = json.loads(request.data.decode('utf-8'))
    previous_uri = data.get('previous_uri')
    uri = data.get('uri')
 
    container = app.sregistry.rename(image_name=previous_uri, 
                                     path=uri)

    message = {'prev': previous_uri, 'uri': uri }
    
    return jsonify({"data": message })
