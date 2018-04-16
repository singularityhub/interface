---
layout: default
title: Getting Started
pdf: true
permalink: /quick-start
toc: false
---

## Quick Start
We are going to be using a <a href="https://hub.docker.com/r/vanessa/tunel/" target="_blank">container</a> 
from Docker Hub, so the only dependency is that you have installed Docker.


### Overview
The basic idea is that we are going to run a <a href="https://hub.docker.com/r/vanessa/tunel/" target="_blank">Docker container</a> that
inside contains the Singularity software (build, and interact with containers), and the 
<a href="https://singularityhub.github.io/sregistry-cli">Singularity Global Client</a> to manage
them. These two work as a tag team, with Singularity handling builds and pulls, and sregistry
handling organization, management, and interaction with endpoints like Google Drive or Globus.

### Start Tunel
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

We will continue the tutorial by trying out a pull and building from a recipe. 
If you want to first see more about globus, see the the [Globus plugin](/interface/plugin-globus) documentation page.

__Why should I map a folder?_
The bind of a local directory (specified with (`-v`)) is so that your containers 
and tiny database can be seen from your host! If you don't map a volume,
the registry will work fine to pull and build containers, but you won't see them on your local machine.
Also, when you stop and remove the container you take the Singularity images with it. 

_Where are the containers?_
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

### Pull Containers
Let's start with the basics. We want to pull a container! If you click on the "pull" button
in the interface, you will be taken to the pull interface. It's very simple - you write the
unique resource identifier (uri) such as `library/ubuntu:latest` in the box in the top
left, and then select the build endpoint, one of:

 - Docker Hub
 - Singularity Hub
 - Nvidia GPU Cloud

![img/quickstart/quickstart-2.png](img/quickstart/quickstart-2.png)

Let's pull an image, `vanessa/algorithms:fireworks`. It's on Docker Hub, so we select that
button:

![img/quickstart/quickstart-3.png](img/quickstart/quickstart-3.png)

Then we click pull!

![img/quickstart/quickstart-4.png](img/quickstart/quickstart-4.png)

When your container is done, you will see a link to view it:

![img/quickstart/quickstart-5.png](img/quickstart/quickstart-5.png)

Clicking the link will show the container view. 

![img/quickstart/quickstart-6.png](img/quickstart/quickstart-6.png)

Right now this is just metadata, but we'd like
to customize this view to be meaningful and fun for you! <a href="https://www.github.com/singularityhub/interface/issues" target="_blank">Let @vsoch know</a> what you would like to see here!

_Where is the container?_
Remember, when you've pulled containers, they are accessible in and outside of the
container.

```bash
# outside the container
$ ls data/.singularity/shub
vanessa  vanessa-algorithms:fireworks.simg
```
```bash
# inside the container (recommended)
$ docker exec -it tunel bash
$ sregistry images
Containers:   [date]   [location]  [client]	[uri]
1  April 16, 2018	local 	   [hub]	vanessa/algorithms:fireworks@7e71bb28a238b74c816a74a12b6509cc
$ container=vanessa/algorithms:fireworks@7e71bb28a238b74c816a74a12b6509cc
$ sregistry get $container
# /root/.singularity/shub/vanessa-algorithms:fireworks.simg
singularity run --contain /root/.singularity/shub/vanessa-algorithms:fireworks.simg --boum
```

### Build Containers
Cool! We can also use Tunel to work with Singularity recipes, which means:

 - Convert from Dockerfile to Singularity, or vice versa
 - Build a Singularity container from the interface!

Click on the Build tab to see the builder interface.

![img/quickstart/quickstart-7.png](img/quickstart/quickstart-7.png)

It's fairly simple. You want to select the correct tab (Dockerfile or Singularity)
that matches the recipe you are starting from. When you click convert, the recipe
will be converted to the other type. When you click build (Singularity only!) you will first
be asked to enter a unique resource identifier (a name for your container)

![img/quickstart/quickstart-8.png](img/quickstart/quickstart-8.png)

and then click "Build Away Merrill!" to start the build. The
recipe will be built, and show you the output in the modal:

![img/quickstart/quickstart-9.png](img/quickstart/quickstart-9.png)

At the bottom, you can again click a link to see the finished container:

![img/quickstart/quickstart-10.png](img/quickstart/quickstart-10.png)

### Logging
Did something go wrong? You can always click on "logs" in the lower right to
see the current server logs.

![img/quickstart/quickstart-11.png](img/quickstart/quickstart-11.png)

## STOPPED HERE - bug that logs/build modal can't show at once

You might next want to transfer your images to your local cluster. To do this,
we recommend using Tunel with the [globus plugin](/interface/plugin-globus).

You might also want to interact with the containers from inside the tunel Docker
container, or from the host! We recommend interaction from within the
Tunel container, discussed next.

If you get an error, you can click "logs" in the lower right to see server logs.
This can help if you need to [submit an issue](https://www.github.com/singularityhub/interface/issues).

![img/logs.png](img/logs.png)

## Singularity Registry
To interact with your database easily, you can shell inside the container. In
the following example, we are still using the container called "tunel."

```
$ docker exec -it tunel bash
root@c4e7d18b362b:/code# sregistry shell
[client|hub] [database|sqlite:////root/.singularity/sregistry.db]
Python 3.6.2 |Anaconda, Inc.| (default, Sep 22 2017, 02:03:08) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: client.speak()
[client|hub] [database|sqlite:////root/.singularity/sregistry.db]
```

Try pulling an image. It will show up in your interface.

```
In [3]: client.pull('vsoch/hello-world')
Progress |===================================| 100.0% 
2.4.3-dist
{
    "data": {
        "attributes": {
            "deffile": "Bootstrap: docker\nFrom: ubuntu:14.04\n\n%labels\nMAINTAINER vanessasaur\nWHATAMI dinosaur\n\n%environment\nDINOSAUR=vanessasaurus\nexport DINOSAUR\n\n%files\nrawr.sh /rawr.sh\n\n%runscript\nexec /bin/bash /rawr.sh\n",
            "help": null,
            "labels": {
                "org.label-schema.usage.singularity.deffile.bootstrap": "docker",
                "MAINTAINER": "vanessasaur",
                "org.label-schema.usage.singularity.deffile": "Singularity",
                "org.label-schema.schema-version": "1.0",
                "WHATAMI": "dinosaur",
                "org.label-schema.usage.singularity.deffile.from": "ubuntu:14.04",
                "org.label-schema.build-date": "2017-10-15T12:52:56+00:00",
                "org.label-schema.usage.singularity.version": "2.4-feature-squashbuild-secbuild.g780c84d",
                "org.label-schema.build-size": "333MB"
            },
            "environment": "# Custom environment shell code should follow\n\nDINOSAUR=vanessasaurus\nexport DINOSAUR\n\n",
            "runscript": "#!/bin/sh \n\nexec /bin/bash /rawr.sh\n",
            "test": null
        },
        "type": "container"
    }
}
[container][new] vsoch/hello-world:latest@ed9755a0871f04db3e14971bec56a33f
Success! /root/.singularity/shub/vsoch-hello-world:latest@ed9755a0871f04db3e14971bec56a33f.simg
Out[3]: '/root/.singularity/shub/vsoch-hello-world:latest@ed9755a0871f04db3e14971bec56a33f.simg'
```

When you interact in the online interface or on the command line, we will be
updating the same database. This is really great, because it means lots of avenues
for interaction between your command line and all those webby things.

Next, read up on [development](/interface/development), which has handy practices
for making changes, and debugging.

<div>
    <a href="/interface/ui"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
