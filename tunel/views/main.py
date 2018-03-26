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



################################################################################
# Actions
################################################################################


@app.route('/action/pull')
def action_pull():

    from shelljob import proc

    # Ensure uri appears once

    container = request.args.get('q')
    uri = request.args.get('uri')
    container = '%s%s' %(uri, container.replace(uri,''))

    print(container)

    # Make sure we use the right client
    os.environ['SREGISTRY_CLIENT'] = uri.replace('://','')
    os.environ.putenv('SREGISTRY_CLIENT', uri.replace('://',''))
    from sregistry.main import get_client
    client = get_client(image=container)
    print(client.client_name)

    try:
        image_file = client.pull(container, force=True)
    except:
        image_file = '''ERROR: manifest unknown, or pull error. 
                        Use docker-compose logs web to see issue!'''
        
    return Response(image_file, mimetype='text/plain')


# Endpoints ####################################################################


@app.route('/google')
def google():
    credentials = get_credentials()
    if credentials == False:
        return flask.redirect(flask.url_for('oauth2callback'))
    elif credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    return render_template("google.html")


@app.route('/google/drive')
def drive():
    credentials = get_credentials()
    if credentials == False or credentials.access_token_expired:
        return google()

    print('now calling fetch')
    all_files = fetch("'root' in parents and mimeType = 'application/vnd.google-apps.folder'", sort='modifiedTime desc')
    s = ""
    for file in all_files:
        s += "%s, %s<br>" % (file['name'],file['id'])
    return render_template("drive.html")


################################################################################
# Containers
################################################################################

@app.route('/pull')
def pull():
    app.sregistry.client_name = 'nvidia'
    nvidia = app.sregistry._get_setting('SREGISTRY_NVIDIA_TOKEN')
    return render_template('pull.html', nvidia=nvidia)


@app.route('/recipe', methods=['GET','POST'])
def generator():

    recipes = {'docker': "FROM ubuntu\r\n",
               'singularity': "From: ubuntu\r\nBootstrap: docker"}
  
    # Default we assume starting with Singularity
    convertType='singularity'

    if request.method == "POST":
        recipe = request.form.get('content')
        recipeKind = request.form.get('recipe-kind')

        # Save recipe to return to user

        recipes[recipeKind] = recipe

        # Import the right parser

        if recipeKind == "singularity":
            convertType = "docker"
            from spython.main.parse import SingularityRecipe as parser
        else:
            from spython.main.parse import DockerRecipe as parser

        # Do the conversion, from string

        parser = parser()
        parser.lines = recipe.split('\n') 
        if hasattr(parser,'load_recipe'):
            parser.load_recipe()        
        parser._parse()
        recipes[convertType] = parser.convert()

    return render_template('recipe.html', recipes=recipes,
                                          recipetype=convertType)


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
