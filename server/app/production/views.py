from flask import jsonify, request
from . import production
from .. import db
from ..models import Product, ProductionRuns, Ingredient

@production.route("/")
def production_home():
    return jsonify({"message": "Welcome to the production home page"})
class ProductsRoutes:

    @production.post('/products')
    def new_product():
        data = request.get_json()
        if request.method == "POST":
            new_product = Product (
            product_id = data.get("product_id"),
            product_name = data.get("product_name"),
            product_price = data.get("product_price"),
            product_description = data.get("product_description")
            )
            db.session.add(new_product)
            db.session.commit()
            return jsonify({"message": "Product added successfully"})
        
    @production.get('/products')
    def view_products():
        all_products = Product.query.all()
        products_list = []
        for product in all_products:
            products_list.append(product.to_json())
        return jsonify(products_list)
    
    @production.get('/products/<int:id>')
    def view_product(id):
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": f"Product of id {id} not found."}), 404
        return jsonify(product.to_json())
    
    @production.put('/products/<int:id>')
    def update_product(id):
        data = request.get_json()
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        product.product_id = data.get("product_id")
        product.product_name = data.get("product_name")
        product.product_price = data.get("product_price")
        product.product_description = data.get("product_description")
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "product updated successfully"})
    
    @production.delete('/products/<int:id>')
    def delete_product(id):
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": f"Product of id {id} not found!"})
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "product deleted successfully"})
    

class ProductionRunsRoutes:

    @production.post('/productionruns')
    def new_run():
        data = request.get_json()
        if request.method == "POST":
            product = Product.query.get(data.get("product_id"))
            if not product:
                return jsonify({"message": "Product not found!"})
            else:
                new_run = ProductionRuns(
                    product_id = data.get("product_id"),
                    flour_kneaded = data.get("flour_kneaded"),
                    oil_used = data.get("oil_used"),
                    packets_produced = data.get("packets_produced")
                )
                db.session.add(new_run)
                db.session.commit()
        return jsonify({"message": "Run added successfully"})
    
    @production.get('/productionruns')
    def view_runs():
        runs = ProductionRuns.query.all()
        runs_list = []
        for run in runs:
            runs_list.append(run.to_json())
        return jsonify(runs_list)
    
    @production.get('/productionruns/<int:id>')
    def view_run(id):
        run = ProductionRuns.query.get(id)
        if not run:
            return jsonify({"message": f"Run not found!"})
        return jsonify(run.to_json())
    
    @production.put('/productionruns/<int:id>')
    def update_run(id):
        data = request.get_json()
        run = ProductionRuns.query.get(id)
        product = Product.query.get(data.get("product_id"))
        if not run:
            return jsonify({"message": f"Run not found!"})
        else:
            if not product:
                return jsonify({"message": "Product not found!"})
            else:
                run.flour_kneaded = data.get("flour_kneaded")
                run.oil_used = data.get("oil_used")
                run.packets_produced = data.get("packets_produced")
                run.product_id = data.get("product_id")
        db.session.add(run)
        db.session.commit()
        return jsonify({"message": "Run updated successfully"})
    
    @production.delete('/productionruns/<int:id>')
    def delete_run(id):
        run = ProductionRuns.query.get(id)
        if not run:
            return jsonify({"message": f"Run not found"})
        db.session.delete(run)
        db.session.commit()
        return jsonify({"message": "Run deleted successfully!"})
    

class IngredientsRoutes:

    @production.post('/ingredients')
    def new_ingredient():
        data = request.get_json()
        if request.method == "POST":
            ingredient = Ingredient(
                ingredient_id = data.get("ingredient_id"),
                ingredient_name = data.get("ingredient_name"),
                ingredient_quantity = data.get("ingredient_quantity"),
                ingredient_measurement = data.get("ingredient_measurement"),
                ingredient_cost = data.get("ingredient_cost")
            )
            db.session.add(ingredient)
            db.session.commit()
        return jsonify({"message": "Ingredient added successfully"})

    @production.get('/ingredients')
    def view_ingredients():
        ingredients = Ingredient.query.all()
        ingredients_list = []
        for ingredient in ingredients:
            ingredients_list.append(ingredient.to_json())
        return jsonify(ingredients_list)
    
    @production.get('/ingredients/<int:id>')
    def view_ingredient(id):
        ingredient = Ingredient.query.get(id)
        if not ingredient:
            return jsonify({"message": "Ingredient not found"})
        return jsonify(ingredient.to_json())
    
    @production.put('/ingredients/<int:id>')
    def update_ingredient(id):
        data = request.get_json()
        ingredient = Ingredient.query.get(id)
        if not ingredient:
            return jsonify({"message": "Ingredient not found"})
        ingredient.ingredient_id = data.get("ingredient_id")
        ingredient.ingredient_name = data.get("ingredient_name")
        ingredient.ingredient_quantity = data.get("ingredient_quantity")
        ingredient.ingredient_measurement = data.get("ingredient_measurement")
        ingredient.ingredient_cost = data.get("ingredient_cost")
        db.session.add(ingredient)
        db.session.commit()
        return jsonify({"message": "Ingredient updated successfully"})
    
    @production.delete('/ingredients/<int:id>')
    def delete_ingredient(id):
        ingredient = Ingredient.query.get(id)
        if not ingredient:
            return jsonify({"Message": "Ingredient not found"})
        return jsonify({"Message": "Ingredient deleted successfully."})