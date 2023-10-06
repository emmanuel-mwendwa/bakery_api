from . import sales
from .. import db
from ..models import Customer
from flask import request, jsonify

class CustomerRoutes:
    @sales.post("/customers")
    def new_customer():
        data = request.get_json()
        new_customer = Customer(
            customer_name = data.get("customer_name"),
            customer_email = data.get("customer_email"),
            customer_phone = data.get("customer_phone"),
            customer_agent_name = data.get("customer_agent_name")
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Customer added successfully"},
            {"customer": new_customer.to_json()}
            ]
        })
    
    @sales.get("/customers")
    def view_customers():
        customers = Customer.query.all()
        customers_list = []
        
        for customer in customers:
            customers_list.append(customer.to_json())
        
        return jsonify({customers_list})
    
    @sales.get("/customers/<int:id>")
    def view_customer(id):
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"message": "Customer not found"})
        
        return jsonify(customer.to_json())
    
    @sales.put("/customers/<int:id>")
    def update_customer():
        data = request.get_json()
        customer = Customer.query.get(id)

        if not customer:
            return jsonify({"message": "Customer not found"})

        customer.customer_name = data.get("customer_name"),
        customer.customer_email = data.get("customer_email"),
        customer.customer_phone = data.get("customer_phone"),
        customer.customer_agent_name = data.get("customer_agent_name")
        
        db.session.add(customer)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Customer updated successfully"},
            {"customer": customer.to_json()}
            ]
        })
    
    @sales.delete("/customers/<int:id>")
    def delete_customer(id):
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"message": "Customer not found"})
        
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully"})
    

class Dispatch:
    pass