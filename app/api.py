from flask_restful import Resource, Api
from singularity.cli import Singularity
from utils import (
    get_container_links,
    get_container_args,
    get_container_labels
)

from main import app
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
