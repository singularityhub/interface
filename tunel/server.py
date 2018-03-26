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
    Flask, 
    url_for
)

from flask_cors import CORS
from flask_wtf.csrf import (
    CSRFProtect, 
    generate_csrf
)

from sregistry.main import Client

import tempfile
import uuid
import os


# SERVER CONFIGURATION #########################################################

class TunelServer(Flask):

    def __init__(self, *args, **kwargs):
        super(TunelServer, self).__init__(*args, **kwargs)
        self.sregistry = Client

app = TunelServer(__name__)
app.config.from_object('tunel.config')


# CORS #########################################################################

cors = CORS(app, origins="http://127.0.0.1",
            allow_headers=["Content-Type", 
                           "Authorization", 
                           "X-Requested-With",
                           "Access-Control-Allow-Credentials"],
            supports_credentials=True)

app.config['CORS_HEADERS'] = 'Content-Type'

csrf = CSRFProtect(app)

import tunel.views

# This is how the command line version will run
def start(port=5000, debug=False):
    bot.info("Nobody ever comes in... nobody ever comes out...")
    app.run(host="localhost", debug=debug, port=port)
