---
layout: default
title: Getting Started
pdf: true
permalink: /quick-start-pull
toc: false
---


# Pull Containers
Let's start with the basics. We want to pull a container! If you click on the "pull" button
in the interface, you will be taken to the pull interface. It's very simple - you write the
unique resource identifier (uri) such as `library/ubuntu:latest` in the box in the top
left, and then select the build endpoint, one of:

 - Docker Hub
 - Singularity Hub
 - Nvidia GPU Cloud

![img/quickstart/quickstart-2.png](img/quickstart/quickstart-2.png)

We will be adding <a href="https://singularityhub.github.io/sregistry-cli/clients" target="_blank">other endpoints</a> 
as they are <a href="{{ site.github }}/issues" target="_blank">requested</a>. 

<br>

Let's pull an image, `vanessa/algorithms:fireworks`. It's on Docker Hub, so we select the first button in the top right.

<br>

![img/quickstart/quickstart-3.png](img/quickstart/quickstart-3.png)

Then we click pull!

![img/quickstart/quickstart-4.png](img/quickstart/quickstart-4.png)

<br>

When your container is done, *the last line* is a link to view it:

<br>

![img/quickstart/quickstart-5.png](img/quickstart/quickstart-5.png)

<br>

Clicking the link will show the container view. 

<br>

![img/quickstart/quickstart-6.png](img/quickstart/quickstart-6.png)

Right now this is just metadata, but we'd like
to customize this view to be meaningful and fun for you! <a href="https://www.github.com/singularityhub/interface/issues" target="_blank">Let @vsoch know</a> what you would like to see here!

<strong>Where is the container?</strong>

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

<br>

<strong>How do I add tokens for Nvidia?</strong>

Nvidia is one of the <a href="https://singularityhub.github.io/sregistry-cli/client-nvidia">
Singularity Global Client plugins</a>. If you try to select it, you will be instructed
to add your token under settings:

![img/quickstart/quickstart-12.png](img/quickstart/quickstart-12.png)

And under settings the box for Nvidia is the only one there :) 

![img/quickstart/quickstart-13.png](img/quickstart/quickstart-13.png)

<br>

When you update it, you can then go back to pull, and the button will not show the same message. Pull Away, Merrill!

<br>

![img/quickstart/quickstart-14.png](img/quickstart/quickstart-14.png)

<br>

Note that Tunel currently uses the 
<a href="https://singularityhub.github.io/sregistry-cli/client-nvidia" target="_blank">Nvidia client</a> 
from Singularity Global client, and not native Singularity as there may still be issues with pulling. 

You are most likely going to want to use Tunel on your laptop where you can easily
build and pull, and then transfer elsewhere that you cannot (like your local cluster resource.) 
We will discuss this more in detail when we talk about [Globus endpoints](/interface/plugin-globus).

<br>
<hr>

<strong>Where to Next?</strong>

 - [Build containers](/interface/quick-start-build)
 - [Logging and utils](/interface/quick-start-utils)
 - [Development](/interface/development)
 - [Quick Start Intro](/interface/quick-start)

<div>
    <a href="/interface/quick-start-build"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
