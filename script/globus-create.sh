#!/bin/bash

usage () {

    echo "Usage:
          docker run <container> -it bash /code/script/globus_create_endpoint.sh
             
          Options:
             --ename: the endpoint name. If not specified, will make a funny one
         
         "
}

ROBOTNAME=$(python /code/script/robotnamer.py)
ENDPOINT="sregistry-${ROBOTNAME}"
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
        --ename)
            shift
            ROBOTNAME="${1:-}"
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

# Globus Personal Endpoint
  
# Bug with getting $USER, see https://github.com/globus/globus-cli/issues/394
export USER="tunel-user"

if [ ! -f "$HOME/.globus.cfg" ]; then
    echo "Logging in to Globus"
    globus login --no-local-server
fi

echo "Generating Globus Personal Endpoint"
token=$(globus endpoint create --personal "${ENDPOINT}" --jmespath 'globus_connect_setup_key'  | tr -d '"') 
/opt/globus/globusconnectpersonal -setup "${token}"

# Export that globus is enabled to config
if ! grep -q PLUGIN_GLOBUS_ENABLED /code/tunel/config.py; then
    echo "PLUGIN_GLOBUS_ENABLED=True" >> /code/tunel/config.py
fi

# Even if we already have a previous robot name, it must correspond
# to naming of this endpoint, so we re-generate (and get a new log file)
echo "ROBOTNAME='${ROBOTNAME}'" >> /code/tunel/config.py

ENDPOINT_ID=$(globus endpoint local-id)
if [ $ENDPOINT_ID != "No Globus Connect Personal installation found." ]; then
    echo "PLUGIN_GLOBUS_ENDPOINT=\"${ENDPOINT_ID}\"" >> /code/tunel/config.py
fi    

# Have we set up config paths yet?
if [ ! -f "$HOME/.globusonline/lta/config-paths" ]; then
    cp /code/tunel/views/plugins/globus/config-paths "${HOME}/.globusonline/lta/config-paths";
fi
