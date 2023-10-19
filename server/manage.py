from app import create_app, db
from flask_migrate import Migrate
from app.models import Product, ProductionRuns, Ingredient, Recipe, RecipeIngredient, Route, Role, Customer, User, Dispatch, DispatchDetails
# from flask_restplus import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify, redirect, request, g, abort
from flask import g
from flask_httpauth import HTTPBasicAuth
import json


app = create_app("default")
migrate = Migrate(app, db)

auth = HTTPBasicAuth()

# @auth.verify_password
# def verify_password(email, password):
#     if email == '':
#         return False
#     user = User.query.filter_by(email = email).first()
#     if not user:
#         return False
#     g.current_user = user
#     return user.verify_password(password)

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


@app.shell_context_processor
def make_shell_processor():
    return dict(
        db=db,
        User=User,
        Product=Product,
        ProductionRuns=ProductionRuns,
        Ingredient=Ingredient,
        Recipe=Recipe,
        RecipeIngredient=RecipeIngredient,
        Route=Route,
        Role=Role,
        Customer=Customer,
        Dispatch=Dispatch,
        DispatchDetails=DispatchDetails
    )

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))
    
@app.route('/')
@app.route("/home")
def index():
    return redirect('http://127.0.0.1:5000/swagger/#/')


if __name__ == "__main__":
    app.run(debug=True)