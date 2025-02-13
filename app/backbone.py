##
## Library Imports
##

# Standard library imports
import json
import sys
import os
import requests
import urllib

# Third-party imports
from flask import (
    session,
    render_template,
    current_app,
    redirect,
)
import jwt

# Function imports
from app.functions import (
    get_oidc_user_info,
    check_permission
)
from app.blueprints.blueprints import (
    get_blueprint_stylesheets,
    get_blueprint_menu_items
)

# Local application/library-specific imports
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app



##
## Setup and Housekeeping
##

# Setup Flask App
app = create_app()
from app import oidc

# Get registered blueprint stylesheets
icon_stylesheets = get_blueprint_stylesheets()
menu_items = get_blueprint_menu_items()

@app.context_processor
def inject_globals():
    try:
        session['id_token'] = oidc.get_access_token()
        user_info = get_oidc_user_info(oidc)
        if user_info.get('client_roles') and user_info.get('roles'):
            unique_roles = set(user_info['roles']) - set(user_info['client_roles'])
            user_info['client_roles'].extend(unique_roles)    
        elif user_info.get('roles') and not user_info.get('client_roles'):
            user_info['client_roles'] = user_info['roles']
    except:
        user_info = {}
        user_info['client_roles'] = []

    app_environment = current_app.config['APP_ENVIRONMENT']
    base_url = current_app.config['LOGIN_URL']

    return {
        'user_info': user_info,
        'check_permission': check_permission,
        'app_environment': app_environment,
        'login_url': base_url,
        'icon_stylesheets': icon_stylesheets,
        'menu_items': menu_items
    }



##
### Setup complete, Routes below
##



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    return render_template('tos.html')


##
### Session Handling
##
@app.route('/login')
@oidc.require_login
def login():
    return redirect('/')



@app.route('/callback')
def oidc_callback():
    return redirect('/')


@app.route('/backchannel_logout')
def logout():
    token = session['oidc_auth_token']['id_token']
    logout_url = current_app.config['OIDC_OP_LOGOUT_ENDPOINT']
    logout_params = {
        'id_token_hint': token,
        'post_logout_redirect_uri': current_app.config['OIDC_REDIRECT_URI']
    }
    # Send keycloak the token and redirect uri so it knows to end the session and which one, we then add the redirect uri to come back to the site after logout
    response = requests.post(logout_url, data=logout_params)
    if response.status_code == 200:
        # clear the session and token locally to avoid issues with any mismatch
        session.clear()
        return redirect('/')
    else:
        # Leaving this for later in case there are issues, having this in prod will make my life easier troubleshooting
        print(f"Failed to log out: {response.status_code}, {response.text}")
        return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
