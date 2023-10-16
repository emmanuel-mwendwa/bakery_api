from flask import request, make_response
from . import auth
from ..models import User

@auth.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.email or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})