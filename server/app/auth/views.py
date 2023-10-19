from flask import request, make_response, g
from . import auth
from ..models import User

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import jsonify, abort

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@auth.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    
    current_user = User.query.filter_by(email=basic_auth.current_user()).first()


    if not current_user.confirmed:

        abort(403, "Account not active")

    return jsonify({'token': current_user.generate_auth_token(), 'expire':'300s'})

@token_auth.verify_token
def token_auth_callback(token):
    
    return User.verify_auth_token(token)


@basic_auth.verify_password
def verify_password(email, password):
    if email == '':
        return False
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

# @app.before_request
# def authentication():
#     email = request.authorization.username if request.authorization else ''
#     password = request.authorization.password if request.authorization else ''

#     if not email:
#         return abort(401)
    
#     user = User.query.filter_by(email=email).first()

#     if not user or not user.verify_password(password):
#         return abort(401)
    
#     g.current_user = user