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
from sregistry.utils import write_file
from spython.main import Client

import contextlib
import itertools
import logging
import os
import json
import re
import sys
import tempfile

def write_temp_recipe(recipe):
    '''write a temporary recipe file, given some recipe text for building.
      
       Parameters
       ==========
       recipe: the text from the interface to write

    '''
    if recipe not in ['', None]:

        # Temporary name for recipe

        tmp = '/tmp/Singularity.%s'% next(tempfile._get_candidate_names())
        recipe = write_file(tmp, recipe)

    return recipe


@app.route('/action/build', methods=["POST"])
def action_build(builder={}):
    '''build a container from a generated recipe.
    '''

    # Post indicates browsing the tree, with an additional path to parse
    if request.method == "POST":

        uri = request.form.get('uri')
        recipe = request.form.get('recipe').replace('\r','')
        app.logger.info('BUILD: %s' %uri)

        # Clean up old recipes
        cleanup('/tmp', "^Singularity.*")
        recipe = write_temp_recipe(recipe)

        if recipe is not None:          

            # When whiteout but is fixed with Singularity...
            image, builder = Client.build(recipe=recipe,
                                          robot_name=True,
                                          sudo=False, stream=True)

            app.logger.info('build %s' %image)
            builder = itertools.chain(builder, [image])

    return Response(builder, mimetype='text/plain')


def cleanup(folder, pattern):
    '''cleanup a folder of files, we only allow the user one build at a time
       so we clean up the build recipes between that.

       Parameters
       ==========
       folder: the directory to look for files in
       pattern: the pattern to match

    '''
    for filey in os.listdir(folder):
        if re.search(pattern, filey):
            file_path = os.path.join(folder, filey)
            app.logger.info('CLEANUP: %s' %file_path)
            os.remove(file_path)


@app.route('/build')
def build():
    '''A build interface for the builders! TODO!
    '''
    app.sregistry.client_name = 'google-compute'
    project = app.sregistry._get_setting('SREGISTRY_NVIDIA_TOKEN')
    credentials = app.sregistry._get_setting('SREGISTRY_NVIDIA_TOKEN')
    return render_template('action/pull.html', nvidia=nvidia)
