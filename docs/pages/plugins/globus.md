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

### Updating Credentials
You might hit a time when your credentials need to be updated! If so, you will
see instructions in the interface.

![img/plugin-globus-update-tokens.png](img/plugin-globus-update-tokens.png)

But if you issued this command when you created the container, since we retrieve
a refresh token you shouldn't need to do this twice. Instead, you should see 
a table of endpoints under scope `my-endpoints` and `shared-with-me`.

![img/globus-endpoints.png](img/globus-endpoints.png)


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

<div>
    <a href="/interface/ui"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/interface/development"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
