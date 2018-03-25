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

import os
import re
import subprocess
import time
from .logman import bot
from glob import glob
from spython.main import Client
from spython.utils import run_command


def get_user():
    '''get_user will return the username. With a moder advanced app,
    we can hook this into a local database.
    '''
    username = run_command('whoami')['message'][0]
    return username.strip('\n').capitalize()


def get_images(install_dir=None,subfolder=None):
    '''get_images is the base/template function to retrieve some set of images
    in the data directory, where subfolder maps to the image folder.
    :param install_dir: the "install directory" of containers, meaning ../data
    '''
    if install_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        install_dir = os.path.abspath(os.path.join(here,'..','data', subfolder))
    containers = dict()
    file_paths = glob("%s/*.img" %(install_dir))
    for container in file_paths:
        container_name = os.path.basename(container)
        containers[container_name] = container
    if len(containers) == 0:
        return None
    return containers


def get_containers(install_dir=None):
    '''get_containers will use will return containers from the containers subfolder
    under data. These are user specifiec containers that the user has built (not to
    be stored as bases)
    '''
    return get_images(install_dir=install_dir,
                      subfolder='containers')


def get_bases(install_dir=None):
    '''get_operating system bases and metadata
    '''
    bases = get_images(install_dir=install_dir,
                       subfolder='bases')
    return bases


def get_container_links(name):
    '''retrieve the links relevant to the container to get various input arguments, etc.
    '''
    api_links = {'args':'/api/container/args/%s' %(name),
                 'selflink':'/api/container/%s' %(name),
                 'labels':'/api/container/labels/%s' %(name)}

    actions = {'view':'/container/%s' %(name),
               'run':'/container/run/%s' %(name)}
    response = {'api':api_links,
                'actions': actions }    
    return response


def get_container_args(image_path,cli=None):
    '''parse the arguments from the container
    :param image_path: the path to the image file
    :param cli: a client. Instantiated if not provided
    '''
    if cli is None:
        cli = Singularity()
    return cli.get_args(image_path)


def get_container_labels(image_path,cli=None):
    '''parse the arguments from the container
    :param image_path: the path to the image file
    :param cli: a client. Instantiated if not provided
    '''
    if cli is None:
        cli = Client
    return cli.get_labels(image_path)


def run_container(image_path,args=None,cli=None):
    '''run the container with one or more args
    '''
    if cli is None:
        cli = Client

    return cli.run(image_path,args=args,contain=True)
    

def sanitize(value):
    '''sanitize is a simple function for sanitizing arguments. All arguments
    come in as strings, and we currently only will support single arguments 
    (without phrases) so all spaces and quotes, and special characters are removed.'''
    return re.sub('[^A-Za-z0-9.:/]+','', value)


def check_install(software,command=None):
    '''check_install will attempt to run the command specified with some argument, 
    and return an error if not installed.
    :param software: the executable to check for
    :param command: the command argument to give to the software (default is --version)
    '''    
    if command == None:
        command = '--version'
    cmd = [software,version]
    version = run_command(cmd,error_message="Cannot find %s. Is it installed?" %software)
    if version != None:
        bot.logger.info("Found %s version %s",software.upper(),version)
        return True
    else:
        return False

def write_json(json_object,filename,mode="w",print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file
    :param json_object: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting   
    '''
    with open(filename,mode) as filey:
        if print_pretty == True:
            filey.writelines(simplejson.dumps(json_object, indent=4, separators=(',', ': ')))
        else:
            filey.writelines(simplejson.dumps(json_object))
    filey.close()
    return filename


def pipe(command):
    '''pipe is the parent function to pip a command and yield
    lines of output
    '''
    if not isinstance(command,list):
        command = [command]

    proc = subprocess.Popen(
        command,             #call something with a lot of output so we can see it
        shell=True,
        stdout=subprocess.PIPE
    )

    for line in iter(proc.stdout.readline,''):
        time.sleep(1)
        #line = line.rstrip() + '<br/>\n'  
        yield line
