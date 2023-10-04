from flask import jsonify, request
from . import production
from .. import db
from ..models import Product

@production.route("/")
def production_home():
    return jsonify({"message": "Welcome to the production home page"})
class ProductsRoutes:

    @production.post('/products')
    def new_product():
        data = request.get_json()
        if request.method == "POST":
            new_product = Product (
            name = data.get("name"),
            price = data.get("price")
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