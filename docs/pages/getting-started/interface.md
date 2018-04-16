---
layout: default
title: The Tunel Interface
pdf: true
permalink: /ui
toc: false
---

# The Tunel Interface
Tunel places an emphasis on simplicity of design. 
The first point of interaction is a table that shows your containers.

![img/home.png](img/home.png)

When you click `pull` you are taken to a page where you can pull containers 
from different endpoints! This will eventually include all
the endpoints that [Singularity Global Client](https://singularityhub.github.io/sregistry-cli/clients)
supports, and for now is your bread and butter endpoints.

![img/pulled.png](img/pulled.png)

When your container is pulled, you can click on the link to see its metadata:

![img/container_details.png](img/container_details.png)

Do you want to interact with containers on remote Globus endpoints, either pulling
from or retrieving from? The [globus plugin](/interface/plugin-globus) makes it 
easy to do that.

![img/globus-endpoints.png](img/globus-endpoints.png)

If you have an issue or need to see the server logs, click "logs" in the lower
right corner.

![img/logs.png](img/logs.png)

The settings panel will help to manage tokens which, if you map the database to 
your computer, will only persist there.

![img/settings.png](img/settings.png)

There is also an interface to make it much easier to generate recipes.

![img/recipes.png](img/recipes.png)

Want to try it out? Check out the [quick start](/interface/quick-start)

<div>
    <a href="/interface"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/quick-start"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
