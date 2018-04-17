---
layout: default
title: Getting Started Developers
pdf: true
permalink: /development
toc: false
---

## Development
To develop, we want to be able to make a change locally and quickly view it. To do this,
we can clone the source repository and map it to the container, and then
restart the container. First, clone the repository:

```bash
git clone https://www.github.com/singularityhub/interface
cd interface
docker build -t vanessa/tunel .
```

Then run the container, mapping the repository base to `/code` where... the code
lives. 

```
$ docker run -p 80:80 -d --name tunel --privileged -v $PWD:/code -v $PWD/data:/root vanessa/tunel start
```

You can shell inside to debug:

```
$ docker exec -it tunel bash
```

or restart the container if the server needs some kind of update...

```
$ docker restart tunel
```

If you hit a server error, you should look at the container logs.

```
$ docker logs tunel
```

In some cases, the Docker container may just show the server error, but not
what caused it, like this:

```
127.0.0.1 - - [26/Mar/2018:19:06:09 +0000] "GET /api/containers HTTP/1.0" 500 37 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
```

In this case, it's good that we have `/code` mapped to our machine, because there will 
be a file called `tunel-server-${ROBOTNAME}.log` in the folder you have mapped to it that gives
the details of the server error. This is the file that the Flask application is logging
to.

## Application Programming Interface
Your Tunel servers an API for all containers, just navigate to [http://127.0.0.1/api/containers](http://127.0.0.1/api/containers) to see it. What does this mean? You can further make applications that use it!

![/interface/img/api.png](/interface/img/api.png)

If you are a developer and would like to see particular developer hints and tutorials here,
please <a href="https://github.com/singularityhub/interface/issues" target="_blank">let me know</a>.

 - [Quick start](/interface/quick-start)
 - [Globus plugin](/interface/plugin-globus)

<div>
    <a href="/interface/quick-start"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/plugin-globus"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
