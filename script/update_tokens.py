#!/usr/bin/env python

from sregistry.main import get_client
import sys

# Default client to update is Globus

client_name = 'globus'
if len(sys.argv) > 1:
    client_name = sys.argv[1]

# Globus

if client_name == 'globus':

    print('Updating Globus Client...')
    globus_client = get_client('globus://')
    if globus_client._tokens_need_update():
        globus_client._list_endpoints()
        print('Tokens updated!')
    else:
        print('Your tokens are up to date.')
