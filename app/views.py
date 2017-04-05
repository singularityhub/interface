from flask import (
    render_template, 
    request,
    Response,
    jsonify
)

from utils import (
    get_containers,
    get_bases,
    get_user,
    get_container_links,
    get_container_args,
    get_container_labels,
    run_container as runc,
    sanitize
)

from shelljob import proc
from random import choice
import os

from main import app

@app.route('/')
def index():
    username = get_user()
    container_names = list(app.containers.keys())
    return render_template('index.html', containers=container_names,
                                         username=username)


@app.route('/bases/update')
def bases_update():

    here = os.path.dirname(os.path.abspath(__file__))
    bases_dir = os.path.abspath(os.path.join(here,'..','data', 'bases'))
    g = proc.Group()
    p = g.run(['/bin/sh','%s/generate_bases.sh' %bases_dir,bases_dir])

    def read_process():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

    return Response(read_process(), mimetype='text/plain')


@app.route('/recipe')
def generator():
    app.bases = get_bases() 
    if app.bases is None:
        return render_template('bases.html')
    return render_template('generator.html')


@app.route('/containers/random')
def random():
    container = choice(list(app.containers.keys()))
    return get_container(container)


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

