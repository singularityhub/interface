---
layout: default
title: Getting Started
pdf: true
permalink: /quick-start-build
toc: true
---

## Build Containers
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

<br>
<hr>

<strong>Where to Next?</strong>

 - [Logging and utils](/interface/quick-start-utils)
 - [Development and API](/interface/development)
 - [Pull containers](/interface/quick-start-pull)
 - [Build containers](/interface/quick-start-build)

<div>
    <a href="/interface/quick-start-utils"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
