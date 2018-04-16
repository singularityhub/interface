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
ROBOTNAME=$(python /code/script/robotnamer.py)
ENDPOINT="sregistry-${ROBOTNAME}"
GLOBUSENABLED="no"
export ROBOTNAME

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

        # Bug with getting $USER, see https://github.com/globus/globus-cli/issues/394
        export USER="tunel-user"

        if [ ! -f "$HOME/.globus.cfg" ]; then
            echo "Logging in to Globus"

            globus login --no-local-server

            echo "Generating Globus Personal Endpoint"
            token=$(globus endpoint create --personal "${ENDPOINT}" --jmespath 'globus_connect_setup_key'  | tr -d '"') 
            /opt/globus/globusconnectpersonal -setup "${token}"

            # Export that globus is enabled to config
            echo "PLUGIN_GLOBUS_ENABLED=True" >> /code/tunel/config.py
            echo "ROBOTNAME='${ROBOTNAME}'" >> /code/tunel/config.py
            echo "PLUGIN_GLOBUS_ENDPOINT=\"$(globus endpoint local-id)\"" >> /code/tunel/config.py
           
        fi

        # Have we set up config paths yet?
        if [ ! -f "$HOME/.globusonline/lta/config-paths" ]; then
            cp /code/tunel/views/plugins/globus/config-paths "${HOME}/.globusonline/lta/config-paths";
        fi
        
    fi

    # If we are doing a restart, the user might not use --globus, check to enable endpoint

    if grep -Fxq "PLUGIN_GLOBUS_ENABLED=True" /code/tunel/config.py
    then

        # When configured, we can start the endpoint
        echo "Starting Globus Connect Personal"
        export USER="tunel-user"
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
