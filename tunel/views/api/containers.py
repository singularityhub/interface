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

from flask_restful import ( Resource, Api )
from flask import jsonify, Response
from tunel.server import app
import json
api = Api(app)

class apiContainers(Resource):
    '''apiContainers
    Main view for REST API to display all available containers
    '''
    def get(self):

        # Generate the url list for each container
        response = {}
        for image in app.sregistry.images():
            response[image.uri] = get_container(image.uri)
        return jsonify(response)

class apiContainer(Resource):
    '''apiContainer
    display metadata and endpoints for a single container
    '''
    def get(self, name):
        return jsonify(get_container(name))


def get_container(name):
    '''get_container is the underlying function to return
       the dictionary response to describe a container.

       Parameters
       ==========
       name: the uri to describe the container

    '''
    # First check complete uri
    containers = [x.uri for x in app.sregistry.images()]
    allcontainers = containers

    # Next try removing the version
    if name not in containers:
        containers = [x.uri.split('@')[0] for x in app.sregistry.images()]  

    # Finally, remove the tag
    if name not in containers:
        containers = [x.uri.split(':')[0] for x in app.sregistry.images()]    
        
    # Last resort, just the namespace
    if name not in containers:
        containers = [x.name for x in app.sregistry.images()]
 
    if name in containers:
         idx = containers.index(name)
         name = allcontainers[idx]         
         return app.sregistry.inspect(name)
    else:
        return {'error':'Not Found'}


api.add_resource(apiContainers,'/api/containers')
api.add_resource(apiContainer,'/api/container/<string:name>')
