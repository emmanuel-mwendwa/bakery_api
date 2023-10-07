from . import sales
from .. import db
from ..models import Customer, Route, User
from flask import request, jsonify


class RoutesRoutes:
    @sales.post("/routes")
    def new_route():
        data = request.get_json()
        sales_agent = User.query.get(data.get("sales_associate_id"))
        if not sales_agent:
            return jsonify({"message": "Sales Agent not found"})
        new_route = Route(
            route_name = data.get("route_name"),
            sales_associate_id = data.get("sales_associate_id")
        )

        db.session.add(new_route)
        db.session.commit()
        return jsonify({"message": [
            {"data": "Route created successfully"},
            {"route": new_route.to_json()}
        ]})
    
    @sales.get("/routes")
    def view_routes():
        routes = Route.query.all()
        routes_list = []

        for route in routes:
            routes_list.append(route.to_json())
        return jsonify(routes_list)
    
    @sales.get("/routes/<int:id>")
    def view_route(id):
        route = Route.query.get(id)
        if not route:
            return jsonify({"message": "Route not found"})
        
        return jsonify(route.to_json())
    
    @sales.put("/routes/<int:id>")
    def update_route(id):
        data = request.get_json()
        route = Route.query.get(id)

        if not route:
            return jsonify({"message": "Route not found"})

        route.route_name = data.get("route_name")
        route.sales_associate_id = data.get("sales_associate_id")
        
        db.session.add(route)
        db.session.commit()

        return jsonify({"message": [
            {"data": "Route updated successfully"},
            {"route": route.to_json()}
            ]
        })
    
    @sales.delete("/routes/<int:id>")
    def delete_route(id):
        route = Route.query.get(id)
        if not route:
            return jsonify({"message": "Route not found"})
        
        db.session.delete(route)
        db.session.commit()
        return jsonify({"message": "Route deleted successfully"})

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
    

class DispatchRoutes:
    pass