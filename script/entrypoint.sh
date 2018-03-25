#!/bin/bash

usage () {

    echo "Usage:
          docker run <container> [start|help]
          docker run -p 80:80 -v /tmp/data:/root/.singularity <container> start

          Commands:
             help: show help and exit
             start: the application
         
          Examples:
              docker run -p 80:80 <container> -v data:/root/.singularity start
         "
}

SREGISTRY_START="no"

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
