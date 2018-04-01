---
layout: default
title: Getting Started
pdf: true
permalink: /quick-start
toc: false
---

## Quick Start
This will map a local folder, data, to save your container registry database and 
containers, and run the container in detached mode. You have to use priviledged
to pull.

```
$ docker run -d -p 80:80 --privileged -v data:/root vanessa/tunel start
```

It's helpful to give it a name, and then use that for logging, inspection, etc.

```
$ docker run --name tunel -d -p 80:80 --privileged -v data:/root vanessa/tunel start
```
```
$ docker logs tunel
$ docker inspect tunel
$ docker restart tunel
```

If you want to authenticate with globus and enable your container as an
endpoint:

```
$ docker run -d -p 80:80 --privileged -v data:/root vanessa/tunel start --globus
```


## Usage
You can use the container directly from Docker Hub. 

```
$ docker run vanessa/tunel help
Usage:
          docker run <container> [start|help]

          Commands:
             help: show help and exit
             start: the application
         
          Examples:
              docker run -d -p 80:80 <container> --privileged -v data:/root/.singularity start
       
```

When you start the container, it will start a web portal to manage your local Singularity Containers. 
This is why you need to map port 80 to your local machine. 

## Container Storage
You also probably want to bind a local
directory (`-v`) so your containers and tiny database are saved. If you don't map a volume,
the registry will work fine to pull containers, but you won't see them on your local machine,
and when you stop and remove the container you take the Singularity images with it. Here
is how to map a directory `data` to root's home:

```
mkdir data
docker run -p 80:80 --privileged -v data:/root vanessa/tunel start
```

You can also skip the volume and just use it on a temporary basis:

```
docker run -p 80:80 --privileged vanessa/tunel start
```

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
