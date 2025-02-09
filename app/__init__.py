from flask import Flask
from flask_oidc import OpenIDConnect
from .configuration_utils import (
    configure_app, 
    load_secrets
)
from .blueprint import register_blueprint

# Define OIDC globally 
# (this needs to be done in __init__.py and the init_app method also needs to be called here)
oidc = OpenIDConnect()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    configure_app(app)
    load_secrets(app)
    oidc.init_app(app)
    register_blueprint(app)
    
    return app
