#!/bin/bash

usage () {

    echo "Usage:
          docker run <container> [start|help]

          Commands:
             help: show help and exit
             start: the application
                      
          Examples:
              docker run --name tunel -d -p 80:80 --privileged -v data:/home/tunel-user/.singularity <container> start
              docker exec -it tunel bash /code/scripts/globus_create_endpoint.sh
         "
}

SREGISTRY_START="no"
ROBOTNAME=$(python /code/script/robotnamer.py)
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

    # If we don't have one already, generate a robot name
    if ! grep -q "ROBOTNAME=" /code/tunel/config.py
    then
        echo "ROBOTNAME='${ROBOTNAME}'" >> /code/tunel/config.py
    fi

    # If we are doing a restart, check if globus enabled

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
