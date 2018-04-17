---
layout: default
title: Getting Started
pdf: true
permalink: /quick-start
toc: false
---

# Quick Start

We are going to be using a <a href="https://hub.docker.com/r/vanessa/tunel/" target="_blank">container</a> 
from Docker Hub, so the only dependency is that you have installed Docker. Inside this container you
are provided with the Singularity software (build, and interact with containers), and the 
<a href="https://singularityhub.github.io/sregistry-cli">Singularity Global Client</a> to manage
them. These two work as a tag team, with Singularity handling builds and pulls, and sregistry
handling organization, management, and interaction with endpoints like Google Drive or Globus.

## Start Tunel
In order to access our containers from the host, we are going to map some local folder `data` to `/root`
in the container. If you want to connect to <a href="https://globus.org" target="_blank">Globus</a> 
then add the  `--globus` flag.

```bash
$ docker run --name tunel -d -p 80:80 --privileged -v $PWD/data:/root vanessa/tunel start --globus
```

Notice how we have given it a name with `--name` so we can easily reference it later as "tunel."
Also notice how we are mapping port 80 from our host? That is because tunel will open a web interface.

```bash
$ docker logs tunel
$ docker inspect tunel
$ docker restart tunel
```

If you started with globus, authenticate your container to access your endpoints, and restart.
If you don't do this now, the interface will tell you to do it later!

```
$ docker exec -it tunel python /code/script/update_tokens.py globus
$ docker restart tunel
```

When you open your browser to [http://127.0.0.1](http://127.0.0.1) you will be 
greeted by the robot!

![img/quickstart/quickstart-1.png](img/quickstart/quickstart-1.png)


<strong>Why should I map a folder?<strong>

The bind of a local directory (specified with `-v`) is so that your containers 
and tiny database can be seen from your host! If you don't map a volume,
the registry will work fine to pull and build containers, but you won't see them on your local machine.
Also, when you stop and remove the container you take the Singularity images with it. 

<strong>Where are the containers?<strong>

Given that you have mapped a volume `data`, any containers that you generate or pull with Tunel will be available
in the folder data/.singularity/shub, which is the storage base. For example:

```bash
$ ls data/.singularity/shub
library                      nvidia
library-busybox:latest.simg  nvidia-tensorflow:17.10.simg
library-centos:6.simg        nvidia-tensorflow:17.11.simg
library-centos:7.simg        vsoch
library-ubuntu:14.04.simg    vsoch-hello-world:latest@ed9755a0871f04db3e14971bec56a33f.simg
library-ubuntu:latest.simg
```

TLDR: 

> The folder mapped to `data` is the primary connection between the Tunel interface
and your host!

We will continue the tutorial by trying out a pull and building from a recipe. 
If you want to first see more about globus, see the the [Globus plugin](/interface/plugin-globus) documentation page.

<strong>Where to Go Next</strong>

 - [Pull containers](/interface/quick-start-pull)
 - [Build containers](/interface/quick-start-build)
 - [Logging and utils](/interface/quick-start-utils)
 - [Development and API](/interface/development)

<hr>
<div>
    <a href="/interface/quick-start-pull"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
