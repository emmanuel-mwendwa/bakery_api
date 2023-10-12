from app import create_app, db
from flask_migrate import Migrate
from app.models import Product, ProductionRuns, Ingredient, Recipe, RecipeIngredient, Route, Role, Customer
# from flask_restplus import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify, redirect, url_for
import json


app = create_app("default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_processor():
    return dict(
        db=db,
        Product=Product,
        ProductionRuns=ProductionRuns,
        Ingredient=Ingredient,
        Recipe=Recipe,
        RecipeIngredient=RecipeIngredient
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