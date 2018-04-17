---
layout: default
title: Globus Plugin
pdf: true
permalink: /plugin-globus
toc: false
---

## Globus
If you started your container with the `--globus` flag, then the container will
be configured with a new Globus endpoint:


```
$ docker run --name tunel -d -p 80:80 --privileged -v data:/root vanessa/tunel start --globus
```

You would then want to authenticate your container to access your endpoints.

```
$ docker exec -it tunel python /code/script/update_tokens.py globus
```

<hr>


## Updating Credentials
You might hit a time when your credentials need to be updated! If so, you will
see instructions in the interface.

![img/plugin-globus-update-tokens.png](img/globus/update-tokens.png)

But if you issued this command when you created the container, since we retrieve
a refresh token you shouldn't need to do this twice. Instead, you should see 
a table of endpoints under scope `my-endpoints` and `shared-with-me`.

![img/globus-endpoints.png](img/globus/globus-endpoints.png)


<br>
<hr>

### Commands
To update your tokens, the easiest way is to issue a command to the docker
container on the command line. A url will be returned that you can open and then
copy paste the code back into the terminal:

```bash
docker exec -it tunel python /code/script/update_tokens.py
```
```python
Updating Globus Client...
Please select an endpoint id to query from
Please go to this URL and login: https://auth.globus.org/v2/oauth2/authorize?client_id=ae32247c-2c17-4c43-92b5-ba7fe9957dbb&redirect_uri=https%3A%2F%2Fauth.globus.org%2Fv2%2Fweb%2Fauth-code&scope=openid+profile+email+urn%3Aglobus%3Aauth%3Ascope%3Atransfer.api.globus.org%3Aall&state=_default&response_type=code&code_challenge=aPNLtTtI8G1AOGBJ7ffxJIT-7NpqGQU8bJvqVWyKTQ0&code_challenge_method=S256&access_type=offline
```
```
Please enter the code you get after login here: xxxxxxxxxxxxxxxxxxxx
```
Then after we enter the code, it gives us a listing of endpoints.

```bash
Globus Endpoints
1  29890592-374e-11e8-b96a-0ac6873fc732	[my-endpoints]	omgtacos
2  1fa46266-34a0-11e8-b93b-0ac6873fc732	[my-endpoints]	sregistry-anxious-nunchucks-2069
3  aa82607a-3466-11e8-b92a-0ac6873fc732	[my-endpoints]	sregistry-dirty-nalgas-8986
4  4e51a760-3462-11e8-b929-0ac6873fc732	[my-endpoints]	sregistry-doopy-underoos-8353
5  2334f658-349f-11e8-b93b-0ac6873fc732	[my-endpoints]	sregistry-evasive-buttface-3847
8  df0b5152-3453-11e8-b929-0ac6873fc732	[my-endpoints]	sregistry-misunderstood-lemur-3519
9  af72ea3c-34a2-11e8-b93b-0ac6873fc732	[my-endpoints]	sregistry-quirky-chair-8749
10 ce0c58e8-3457-11e8-b929-0ac6873fc732	[my-endpoints]	sregistry-tart-latke-6416
11 efe591ca-374d-11e8-b96a-0ac6873fc732	[my-endpoints]	tmpep
12 74f0809a-d11a-11e7-962c-22000a8cbd7d	[my-endpoints]	vanessasaurus-endpoint
13 9ec1db6a-5052-11e7-bdb7-22000b9a448b	[shared-with-me]	Karl Transfer
Tokens updated!

```

The refresh token should now be cached so if you run it again, it will tell you that you
are good to go!

```bash
$ docker exec -it tunel python /code/script/update_tokens.py
$ Updating Globus Client...
$ Your tokens are up to date.
```

We use the same credentials in the interface, so you can refresh the page and
use your Globus endpoint. 

## Your Endpoints
Globus groups endpoints based on scope. The default Globus plugin page will show you
all endpoints with scope `shared-with-me` and `my-endpoints`. You might not have many,
it's ok! What you likely want to do is use the search box at the top to search for
endpoints that you are interested in. For example, since I am a Stanford person,
I might search for Stanford and discover many Globus endpoints installed across 
Stanford resources:

![img/globus/stanford-endpoints.png](img/globus/stanford-endpoints.png)

Your access to these endpoints depends upon (typically) you having an account on each
server. If you don't have access to a particular endpoint, you could try reaching out
to the contact email to ask if it might be possible. More likely, you will need to
click on an endpoint of interest to authenticate for the endpoint in the Globus portal.
When this works and you can "see" the endpoint from the Tunel client, there will be a 
green "active" button as we see in the picture above. Let's click on the "SRCC Sherlock"
endpoint and look closer.

![img/globus/stanford-sherlock.png](img/globus/stanford-sherlock.png)

What you see here is a simple file browser. The endpoint is on the left, and in this case,
we are looking at my `$SCRATCH` on Sherlock. The Sregistry local images are in the box on
the right. 

<hr><br>

## Transfer
For either, I can select a local image and click the left arrow to transfer 
it to the cluster:

![img/globus/transfer-to-sherlock.png](img/globus/sherlock-transfer-to.png)

or I can click on an image file row in the left, and when I do so, a right arrow
appears that I can click to transfer the selected container to my local registry!

![img/globus/transfer-from-sherlock.png](img/globus/sherlock-transfer-from.png)

Note that the transfer itself is dependent on Globus (it doesn't
happen immediately) so the result may take a few minutes. If I click on the view
task link, I can watch progress.

![img/globus/transfer-activity.png](img/globus/transfer-activity.png)

When the transfer is absolutely done, depending on your preferences, you are likely to
get an email with the status.

![img/globus/globus-email.png](img/globus/globus-email.png)

Once you receive this notification, you can be sure that the task is considered complete,
and it will appear in the Globus API endpoint for successful transfers for your
client to find and finish the final import of the container. You will see a message
that the task was found as finished, and the container transfer done if done from
remote to local:

![img/globus/new-container.png](img/globus/new-container.png)

If you transferred to a remote, you should be able to see the file 
there in the interface.

![img/globus/after-transfer.png](img/globus/after-transfer.png)

If you want to change folders, just click on a folder icon in the list to navigate.
Here I am after clicking on the folder `.singularity`.


![img/globus/navigate.png](img/globus/navigate.png)

<hr><br>

## Debugging

<strong>What happens if the transfer doesn't work?</strong>
You might first look at the server logs. See if your tunel server has an issues:

```bash

docker logs tunel
```

If everything looks good there, you can check the application logs in the interface
or via the command line:

```bash

# Where are the logs?
$ docker exec it tunel bash
$ docker exec tunel ls /tmp
Singularity.adqtcmtb
gunicorn-access.log
gunicorn.log
nginx-access.log
nginx-error.log
nginx.pid
tunel-server-blank-muffin-0742.log
tunel-server-bumfuzzled-despacito-2591.log

```
```bash
$ docker exec tunel cat /tmp/tunel-server-bumfuzzled-despacito-2591.log
```

That will usually give some insight about the issue! You can also check the
configuration, and make sure that you see that Globus is enabled, you have an `ENDPOINT_ID`
and `ROBOTNAME`:

```bash
$ docker exec tunel cat /code/tunel/config.py
PLUGIN_GLOBUS_ENABLED=True
ROBOTNAME="spurious-meatball"
PLUGIN_GLOBUS_ENDPOINT="af72ea3c-34a2-11e8-b93b-0ac6873fc732"
```

If any of those are missing, check out the commands that need to be run in the
[entrypoint.sh](https://github.com/singularityhub/interface/blob/master/script/entrypoint.sh#L68) script for Globus, and you can interactively run
them to create or update the endpoint or credentials. Usually this might be the case
if you didn't originally create your container to be Globus enabled. If you have any
trouble, please <a href="https://www.github.com/singularityhub/interface/issues" target="_blank">reach out</a>.

<div>
    <a href="/interface/quick-start"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
