'''

Copyright (c) 2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
