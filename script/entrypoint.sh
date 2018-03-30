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
              docker run -d -p 80:80 --privileged -v data:/root/.singularity <container> start
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
        --enable-globus)
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

        if [ ! -f "ls ${HOME}/.globus.cfg" ]; then
            echo "Logging in to Globus"

            globus login --no-local-server

            echo "Generating Globus Personal Endpoint"
            response=$(globus endpoint create --personal "${ROBOTNAME}")
 
            # Bad party trick to get setup key, last in response
            for token in ${response}; do token=$token;done
            /opt/globus/globusconnectpersonal -setup "${token}"
        fi

    fi

    echo "Starting Registry Portal"
    echo
    service nginx start
    touch /var/log/gunicorn.log
    touch /var/log/gunicorn-access.log
    tail -n 0 -f /var/log/gunicorn*.log &

    exec  /opt/conda/bin/gunicorn tunel.wsgi:app \
                  --bind 0.0.0.0:5000 \
                  --workers 5 \
                  --log-level=info \
                  --timeout 900 \
                  --log-file=/var/log/gunicorn.log \
                  --access-logfile=/var/log/gunicorn-access.log  \
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
