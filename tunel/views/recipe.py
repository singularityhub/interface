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
