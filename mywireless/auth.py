import functools
import uuid
from flask import current_app, g, redirect, render_template, request, session, url_for
from flask_oauthlib.client import OAuth


class OAuthSignIn(object):
    credentials = current_app.config['OAUTH_CREDENTIALS']
    parameters = current_app.config['OAUTH_PARAMETERS']
