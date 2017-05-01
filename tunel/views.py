from flask import (
    render_template, 
    request,
    Response,
    jsonify
)

from utils import get_user
from auth import get_credentials
from shelljob import proc
from random import choice
import os

from main import app

@app.route('/')
def index():
    username = get_user()
    return render_template('index.html', username=username)


@app.route('/browser')
def browser():
    return render_template("browser.html")

@app.route('/google')
def google():
    credentials = get_credentials()
    if credentials == False:
        return flask.redirect(flask.url_for('oauth2callback'))
    elif credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    return render_template("google.html")


@app.route('/google/drive')
def drive():
    credentials = get_credentials()
    if credentials == False or credentials.access_token_expired:
        return google()

    print('now calling fetch')
    all_files = fetch("'root' in parents and mimeType = 'application/vnd.google-apps.folder'", sort='modifiedTime desc')
    s = ""
    for file in all_files:
        s += "%s, %s<br>" % (file['name'],file['id'])
    return render_template("drive.html")
