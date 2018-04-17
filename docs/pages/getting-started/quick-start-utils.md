---
layout: default
title: Getting Started
pdf: true
permalink: /quick-start-utils
toc: false
---

Once you've finished pulls and builds, you will have a local registry of containers!
You can browse to [http://127.0.0.1/]() to see your updated table. Do you want to rename
any of the containers? Just click the box

![img/quickstart/quickstart-15.png](img/quickstart/quickstart-15.png)

type the new name, and confirm your decision. You'll see the change in the interface
and a message that it was done.

![img/quickstart/quickstart-16.png](img/quickstart/quickstart-16.png)



# Logging

Did something go wrong? You can always click on "logs" in the lower right to
see the current server logs.

![img/quickstart/quickstart-11.png](img/quickstart/quickstart-11.png)

You might next want to transfer your images to your local cluster. To do this,
we recommend using Tunel with the [globus plugin](/interface/plugin-globus).

You might also want to interact with the containers from inside the tunel Docker
container, or from the host! We recommend interaction from within the
Tunel container, discussed next.

<br>
<hr>


## Singularity Registry
The Tunel interface is running a local Singularity Global Client, and this is
the <a href="https://singularityhub.github.io/sregistry-cli" target="_blank">containertools solution</a> 
for the single user to have a small local database of organized conatainers. 
This is a smaller database compared to the more substantial, open source
<a href="https://singularityhub.github.io/sregistry" target="_blank">Singularity Registry</a>
that your institution might choose to deploy. This means that to interact with your 
database easily, you can shell inside the container. In
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

The client above that is loaded by default with `sregistry shell` is the
<a href="https://singularityhub.github.io/sregistry-cli" target="_blank">Singularity Global Client</a>.
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

Next, you can read up on [development](/interface/development), which has handy practices
for making changes, and debugging, or you can read about [the Globus endpoint](/interface/plugin-globus)
for easily transferring containers between your local computer and cluster endpoints.

<strong>Where to Next?</strong>

 - [Development and API](/interface/development)
 - [Quick Start Intro](/interface/quick-start)
 - [Pull containers](/interface/quick-start-pull)
 - [Build containers](/interface/quick-start-build)

<div>
    <a href="/interface/quick-start-build"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
