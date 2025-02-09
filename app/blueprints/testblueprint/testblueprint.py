from flask import (
    Blueprint, 
    render_template, 
    request
)

from app import oidc

testblueprint = Blueprint('testblueprint', __name__, template_folder='templates', static_folder='static')


@testblueprint.route('/testblueprint', methods = ['GET', 'POST'])
@oidc.require_login
def test_home():
    if request.method == 'GET':
        return render_template('testblueprints.html')