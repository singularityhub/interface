#!/bin/bash

usage () {

    echo "Usage:
          docker run <container> [start|help]

          Commands:
             help: show help and exit
             start: the application
             
          Options:
             --ename: the endpoint name. If not specified, will make a funny one
             --globus: enable globus login
         
          Examples:
              docker run -d -p 80:80 --privileged -v data:/home/tunel-user/.singularity <container> start
         "
}

SREGISTRY_START="no"
ROBOTNAME="sregistry-$(python /code/script/robotnamer.py)"
GLOBUSENABLED="no"

if [ $# -eq 0 ]; then
    usage
    exit
fi

while true; do
    case ${1:-} in
        -h|--help|help)
            usage
            exit
        ;;
        -s|--start|start)
            SREGISTRY_START="yes"
            shift
        ;;
        --ename)
            shift
            ROBOTNAME="${1:-}"
            shift
        ;;
        --globus)
            GLOBUSENABLED="yes"
            shift
        ;;
        -*)
            echo "Unknown option: ${1:-}"
            exit 1
        ;;
        *)
            break
        ;;
    esac
done

# Are we starting the server?

if [ "${SREGISTRY_START}" == "yes" ]; then

    # Globus Personal Endpoint
  
    if [ "${GLOBUSENABLED}" == "yes" ]; then

        if [ ! -f "$HOME/.globus.cfg" ]; then
            echo "Logging in to Globus"

            globus login --no-local-server

            echo "Generating Globus Personal Endpoint"
            response=$(globus endpoint create --personal "${ROBOTNAME}")
 
            # Bad party trick to get setup key, last in response
            for token in ${response}; do token=$token;done

            # Bug with getting $USER, see https://github.com/globus/globus-cli/issues/394
            export USER="tunel-user"
            /opt/globus/globusconnectpersonal -setup "${token}"

            # Export that globus is enabled to config
            echo "PLUGIN_GLOBUS_ENABLED=True" >> /code/tunel/config.py
           
        fi

        # Have we set up config paths yet?
        if [ ! -f "$HOME/.globusonline/lta/config-paths" ]; then
            echo "${HOME}/.singularity/shub,0,1" >> "${HOME}/.globusonline/lta/config-paths"
        fi

        # When configured, we can start the endpoint
        echo "Starting Globus Connect Personal"
        /opt/globus/globusconnectpersonal -start &
        
    fi

    echo "Starting Registry Portal"
    echo
    service nginx start
    touch /tmp/gunicorn.log
    touch /tmp/gunicorn-access.log
    tail -n 0 -f /tmp/gunicorn*.log &

    exec  /opt/conda/bin/gunicorn tunel.wsgi:app \
                  --bind 0.0.0.0:5000 \
                  --workers 5 \
                  --log-level=info \
                  --timeout 900 \
                  --log-file=/tmp/gunicorn.log \
                  --access-logfile=/tmp/gunicorn-access.log  \
            "$@" & service nginx restart

    # simple manual command could be
    # service nginx start
    # /opt/conda/bin/gunicorn -w 2 -b 0.0.0.0:5000 --timeout 900 --log-level debug tunel.wsgi:app
    # service nginx restart

    # Keep container running if we get here
    tail -f /dev/null
    exit
else
    usage
fi
