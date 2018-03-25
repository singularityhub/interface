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


from flask_restful import Resource, Api
from tunel.utils import (
    get_container_links,
    get_container_args,
    get_container_labels
)

from tunel.server import app
api = Api(app)

class apiContainers(Resource):
    '''apiContainers
    Main view for REST API to display all available containers
    '''
    def get(self):
        # Generate the url list for each container
        response = {}
        for cname,cpath in app.containers:
            response[cname] = url_for('.api_container',cname)
        return response


class apiContainerArgs(Resource):
    '''apiContainerArgs
    '''
    def get(self, name):
        if name in app.containers:
            image_path = app.containers[name]
            return get_container_args(image_path,cli=app.cli)
        else:
            return {'error':'Not Found'}

class apiContainerLabels(Resource):
    '''apiContainerLabels
    '''
    def get(self, name):
        if name in app.containers:
            image_path = app.containers[name]
            return get_container_labels(image_path,cli=app.cli)
        else:
            return {'error':'Not Found'}


class apiContainer(Resource):
    '''apiContainer
     display metadata and endpoints for a container
    '''
    def get(self, name):
        if name in app.containers:
            response = dict()
            image_path = app.containers[name]
            response['links'] = get_container_links(name) 
            response['args'] = get_container_args(image_path,cli=app.cli)
            response['labels'] = get_container_labels(image_path,cli=app.cli)
            response['name'] = name
            return response
        else:
            return {'error':'Not Found'}

    
api.add_resource(apiContainers,'/api/containers')
api.add_resource(apiContainer,'/api/container/<string:name>')
api.add_resource(apiContainerArgs,'/api/container/args/<string:name>')
api.add_resource(apiContainerLabels,'/api/container/labels/<string:name>')
