import functools
import uuid
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
from flask_oauthlib.client import OAuth
from werkzeug.exceptions import abort
from mywireless import auth
from mywireless.auth import OAuthSignIn


bp = Blueprint('mw', __name__)
oauth = OAuthSignIn()

OAUTH = OAuth(current_app)
MSGRAPH = OAUTH.remote_app(
    'mwhqweb',
    consumer_key=oauth.credentials['CLIENT_ID'],
    consumer_secret=oauth.credentials['CLIENT_SECRET'],
    request_token_params={'scope': oauth.parameters['SCOPES']},
    base_url=oauth.parameters['RESOURCE'] + oauth.parameters['API_VERSION'] + '/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=oauth.parameters['AUTHORITY_URL'] + oauth.parameters['TOKEN_ENDPOINT'],
    authorize_url=oauth.parameters['AUTHORITY_URL'] + oauth.parameters['AUTH_ENDPOINT']
)


@MSGRAPH.tokengetter
def get_token():
    """Called by flask_oauthlib.client to retrieve current access token."""
    return session.get('microsoft_token')


@bp.route('/')
def index():
    return render_template('mywireless/index.html')


@bp.route('/login')
def login():
    if 'microsoft_token' in session:
        return redirect(url_for('mw.index'))
    parameters = oauth.parameters
    session['state'] = str(uuid.uuid4())
    return MSGRAPH.authorize(callback=parameters['REDIRECT_URI'], state=session['state'])


@bp.route('/login/authorized')
def authorized():
    if str(session['state']) != str(request.args['state']):
        print('Session State: {}'.format(str(session['state'])))
        print('Request State: {}'.format(str(request.args['state'])))
        raise Exception('state returned to redirect URL does not match!')

    response = MSGRAPH.authorized_response()

    if response is None:
        return 'Access Denied: Reason={}, Error={}'.format(response.get('error'), response.get('error_description'))

    print('Response: ' + str(response))

    session['microsoft_token'] = response['access_token']
    headers = {'SdkVersion': 'mwhqweb',
               'x-client-SKU': 'mwhqweb',
               'client-request-id': str(uuid.uuid4()),
               'return-client-request-id': 'true'}
    user_data = MSGRAPH.get('me', headers=headers).data
    group_membership = MSGRAPH.get('me/memberOf', headers=headers).data
    session['user_id'] = user_data['displayName']
    session['user_groups'] = [group['id'] for group in group_membership['value']]
    return redirect(url_for('human_resources.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('mw.index'))

        return view(**kwargs)

    return wrapped_view


def hr_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or 'ab95afb9-e27c-41f4-9737-36cf1fed467e' not in session.get('user_groups'):
            return redirect(url_for('mw.index'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('mw.index'))


