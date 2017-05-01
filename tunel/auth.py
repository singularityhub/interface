import flask
from oauth2client import client
from oauth2client.file import Storage
import pwd
import os

from . import app

# Supporting Functions

def get_home():
    return pwd.getpwuid(os.getuid())[5]

def get_credentials():
    userhome = get_home()
    srcc = os.path.join(userhome,".srcc") 
    if not os.path.exists(srcc):
        os.mkdir(srcc)
    credential_path = os.path.join(srcc,"gdrive-migration-credentials.json") 
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("Credentials not found.")
        return False
    else:
        print("Credentials fetched successfully.")
        return credentials



# Auth views

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets('client_id.json',
                                          scope='https://www.googleapis.com/auth/drive',
                                          redirect_uri=flask.url_for('oauth2callback', _external=True))

    flow.params['include_granted_scopes'] = 'true'
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        open('credentials.json','w').write(credentials.to_json())
        return flask.redirect(flask.url_for('index'))
