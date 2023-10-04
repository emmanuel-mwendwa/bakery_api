from flask import jsonify, request
from . import production
from .. import db
from ..models import Product, ProductionRuns

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
    
    @production.delete('/productionruns/<int:id>')
    def delete_run(id):
        run = ProductionRuns.query.get(id)
        if not run:
            return jsonify({"message": f"Run not found"})
        db.session.delete(run)
        db.session.commit()
        return jsonify({"message": "Run deleted successfully!"})