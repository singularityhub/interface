# Singularity Recipe

## Introduction
Manager and recipe generator for local Singularity containers


## Deployment
You should clone the repo, and build the container (or you can also just clone and then use docker-compose and it will be pulled from Docker Hub).


```bash
git clone https://www.github.com/singularityware/singularity-recipe
cd singularity-recipe
docker build -t vanessa/singularity-recipe .
```

## Deployment
You can use docker compose to deploy:

```bash          
docker-compose up -d
```
and then go to `127.0.0.1` (localhost).


## Endpoints
Here are some useful endpoints:

### Views
 - `/`: the root will show all containers available. When the user selects, he/she is taken to a screen to see input arguments. 
 - `/containers/random`: will return a random container
 - `/container/container.img`: will show metadata about a container.

### API
The following are considered API, meaning they return a text or json response, not intended for the user to interact with.

 - `/api/containers`: a list of all available containers
 - `/api/container/<string:name>`: a json object with container args, labels, and links.
 - `/api/container/args/<string:name>`: json of just container args
 - `/api/container/labels/<string:name>`: json of juist container labels
 - `/container/run/container.img`: Is the base for running a container, this one would be container.img. Arguments can be added as POST (eg, `?name=Amy`)
